"""Document Q&A with citations and abstention.

Baseline: BM25 retrieval over paragraph chunks + extractive answer (best
matching sentence). Optional model mode (PAS_LLM) writes the answer from the
retrieved chunks only and must cite a retrieved chunk id, or we abstain.

Standalone: this file has zero imports outside the Python standard library.
Copy this whole `doc_qa/` folder anywhere and it keeps working.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Protocol

DATA_DIR = Path(__file__).parent / "data"
ABSTAIN = "I can't find that in the documentation."
PROMPT = """Answer the question using ONLY the context. Cite the chunk id in square brackets, e.g. [billing.md#1].
If the context does not contain the answer, reply exactly: {abstain}

Context:
{context}

Question: {question}
Answer:"""

# --- lexical retrieval (tokenize/sentences/BM25) ---------------------------

STOPWORDS = frozenset(
    "a an and are as at be by can do does for from has have how i in is it its of on or "
    "our that the their this to was we what when where which who why will with you your".split()
)
_TOKEN = re.compile(r"[a-z0-9]+")
_SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _stem(token: str) -> str:
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 2 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def tokenize(text: str) -> list[str]:
    return [_stem(t) for t in _TOKEN.findall(text.lower()) if t not in STOPWORDS]


def sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE.split(text.strip()) if s.strip()]


class BM25:
    """Okapi BM25 over a {doc_id: text} mapping."""

    def __init__(self, docs: dict[str, str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tokens = {doc_id: tokenize(text) for doc_id, text in docs.items()}
        self.avg_len = sum(map(len, self.tokens.values())) / max(len(self.tokens), 1)
        df = Counter(term for toks in self.tokens.values() for term in set(toks))
        n = len(self.tokens)
        self.idf = {term: math.log(1 + (n - freq + 0.5) / (freq + 0.5)) for term, freq in df.items()}

    def score(self, query: str, doc_id: str) -> float:
        toks = self.tokens[doc_id]
        counts = Counter(toks)
        norm = self.k1 * (1 - self.b + self.b * len(toks) / (self.avg_len or 1))
        return sum(
            self.idf[t] * counts[t] * (self.k1 + 1) / (counts[t] + norm)
            for t in set(tokenize(query))
            if t in counts
        )

    def search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        scored = ((doc_id, self.score(query, doc_id)) for doc_id in self.tokens)
        hits = sorted((h for h in scored if h[1] > 0), key=lambda h: (-h[1], h[0]))
        return hits[:k]


# --- optional LLM provider (used only when PAS_LLM is set) -----------------


class LLM(Protocol):
    def complete(self, prompt: str, system: str = "") -> str: ...


class StubLLM:
    """Deterministic fake for tests: maps prompt -> response with a function."""

    def __init__(self, responder: Callable[[str], str]):
        self.responder = responder
        self.calls: list[str] = []

    def complete(self, prompt: str, system: str = "") -> str:
        self.calls.append(prompt)
        return self.responder(prompt)


def _response_text(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("provider response content must be text")
    return value


class _HTTPLLM:
    def __init__(self, url: str, model: str, headers: dict[str, str] | None = None, timeout: int = 120):
        self.url, self.model, self.timeout = url, model, timeout
        self.headers = {"Content-Type": "application/json", **(headers or {})}

    def _post(self, payload: dict) -> dict:
        req = urllib.request.Request(self.url, json.dumps(payload).encode(), self.headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.load(resp)


class OllamaLLM(_HTTPLLM):
    def __init__(self, model: str, host: str = "http://localhost:11434"):
        super().__init__(f"{host}/api/generate", model)

    def complete(self, prompt: str, system: str = "") -> str:
        body = {"model": self.model, "prompt": prompt, "system": system, "stream": False, "options": {"temperature": 0}}
        return _response_text(self._post(body)["response"])


class OpenAICompatibleLLM(_HTTPLLM):
    def __init__(self, model: str, base_url: str, api_key: str):
        super().__init__(f"{base_url.rstrip('/')}/chat/completions", model, {"Authorization": f"Bearer {api_key}"})

    def complete(self, prompt: str, system: str = "") -> str:
        messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
        body = {"model": self.model, "messages": messages, "temperature": 0}
        return _response_text(self._post(body)["choices"][0]["message"]["content"])


def from_env(provider: str | None = None) -> LLM | None:
    """Return the configured provider, or None to use the offline baseline."""
    provider = (provider if provider is not None else os.getenv("PAS_LLM", "")).strip().lower()
    model = os.getenv("PAS_MODEL", "llama3.2:3b")
    if not provider:
        return None
    if provider == "ollama":
        return OllamaLLM(model, os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    if provider == "openai":
        return OpenAICompatibleLLM(model, os.environ["PAS_BASE_URL"], os.environ["PAS_API_KEY"])
    raise ValueError(f"unknown PAS_LLM provider: {provider!r} (use 'ollama' or 'openai')")


# --- document Q&A ------------------------------------------------------------


@dataclass
class Answer:
    text: str
    citations: list[str] = field(default_factory=list)
    retrieved: list[str] = field(default_factory=list)

    @property
    def abstained(self) -> bool:
        return not self.citations


def load_chunks(data_dir: Path = DATA_DIR) -> list[tuple[str, str]]:
    """Split each markdown file into paragraph chunks with stable ids (file#n)."""
    chunks = []
    for path in sorted(data_dir.glob("*.md")):
        paragraphs = [p.strip() for p in path.read_text().split("\n\n") if p.strip() and not p.startswith("#")]
        chunks += [(f"{path.name}#{i}", text) for i, text in enumerate(paragraphs, start=1)]
    return chunks


class DocQA:
    def __init__(
        self,
        chunks: list[tuple[str, str]],
        llm: LLM | None = None,
        min_score: float = 2.5,
        min_coverage: float = 0.5,
        k: int = 3,
    ):
        self.chunks = dict(chunks)
        self.index = BM25(self.chunks)
        self.llm, self.min_score, self.min_coverage, self.k = llm, min_score, min_coverage, k

    def retrieve(self, question: str) -> list[tuple[str, float]]:
        return self.index.search(question, self.k)

    def coverage(self, question: str, chunk_id: str) -> float:
        """Share of question terms that appear in the chunk: a cheap 'is this really about it?' check."""
        query = set(tokenize(question))
        return len(query & set(self.index.tokens[chunk_id])) / len(query) if query else 0.0

    def answer(self, question: str) -> Answer:
        hits = self.retrieve(question)
        retrieved = [chunk_id for chunk_id, _ in hits]
        if not hits or hits[0][1] < self.min_score:
            return Answer(ABSTAIN, retrieved=retrieved)
        if self.coverage(question, hits[0][0]) < self.min_coverage:
            return Answer(ABSTAIN, retrieved=retrieved)
        if self.llm:
            return self._generate(question, retrieved)
        return self._extract(question, hits[0][0], retrieved)

    def _extract(self, question: str, chunk_id: str, retrieved: list[str]) -> Answer:
        query = set(tokenize(question))
        best = max(sentences(self.chunks[chunk_id]), key=lambda s: len(query & set(tokenize(s))))
        return Answer(best, [chunk_id], retrieved)

    def _generate(self, question: str, retrieved: list[str]) -> Answer:
        context = "\n".join(f"[{cid}] {self.chunks[cid]}" for cid in retrieved)
        reply = self.llm.complete(PROMPT.format(abstain=ABSTAIN, context=context, question=question)).strip()
        cited = [cid for cid in re.findall(r"\[([^\]]+)\]", reply) if cid in retrieved]
        if not cited:  # uncited or hallucinated citation -> do not trust it
            return Answer(ABSTAIN, retrieved=retrieved)
        return Answer(reply, list(dict.fromkeys(cited)), retrieved)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("question")
    args = parser.parse_args()
    answer = DocQA(load_chunks(), llm=from_env()).answer(args.question)
    print(answer.text)
    print("sources:", ", ".join(answer.citations) or "none (abstained)")


if __name__ == "__main__":
    main()
