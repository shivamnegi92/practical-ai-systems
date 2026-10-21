"""Decompose a multi-part question and require every part to be answered before replying.

Splits on " and " or a mid-string "?" to get sub-questions, answers each
with a small bundled BM25 + extractive DocQA baseline, and abstains for the
whole question unless every sub-question is independently answered.

Standalone: this file has zero imports outside the Python standard library;
it carries its own copy of the BM25/DocQA baseline and sample documents.
"""
from __future__ import annotations

import argparse
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
ABSTAIN = "I can't find that in the documentation."
SPLIT_PATTERN = re.compile(r"\s+and\s+|\?\s*(?=\w)", re.I)

# --- lexical retrieval (tokenize/sentences/BM25) ---------------------------

_STOPWORDS = frozenset(
    "a an and are as at be by can do does for from has have how i in is it its of on or "
    "our that the their this to was we what when where which who why will with you your".split()
)
_TOKEN_RE = re.compile(r"[a-z0-9]+")
_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def _stem(token: str) -> str:
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 2 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def tokenize(text: str) -> list[str]:
    return [_stem(t) for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS]


def sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_RE.split(text.strip()) if s.strip()]


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


# --- single-hop document Q&A (extractive baseline only) ---------------------


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
    def __init__(self, chunks: list[tuple[str, str]], min_score: float = 2.5, min_coverage: float = 0.5, k: int = 3):
        self.chunks = dict(chunks)
        self.index = BM25(self.chunks)
        self.min_score, self.min_coverage, self.k = min_score, min_coverage, k

    def retrieve(self, question: str) -> list[tuple[str, float]]:
        return self.index.search(question, self.k)

    def coverage(self, question: str, chunk_id: str) -> float:
        query = set(tokenize(question))
        return len(query & set(self.index.tokens[chunk_id])) / len(query) if query else 0.0

    def answer(self, question: str) -> Answer:
        hits = self.retrieve(question)
        retrieved = [chunk_id for chunk_id, _ in hits]
        if not hits or hits[0][1] < self.min_score:
            return Answer(ABSTAIN, retrieved=retrieved)
        if self.coverage(question, hits[0][0]) < self.min_coverage:
            return Answer(ABSTAIN, retrieved=retrieved)
        query = set(tokenize(question))
        best = max(sentences(self.chunks[hits[0][0]]), key=lambda s: len(query & set(tokenize(s))))
        return Answer(best, [hits[0][0]], retrieved)


# --- multi-hop decomposition --------------------------------------------------


def decompose(question: str) -> list[str]:
    cleaned = [re.sub(r"[\s?]+$", "", part.strip()) for part in SPLIT_PATTERN.split(question)]
    return [part + "?" for part in cleaned if part]


def answer_multi_hop(question: str, qa: DocQA | None = None) -> dict:
    qa = qa or DocQA(load_chunks())
    sub_questions = decompose(question)
    sub_answers = [qa.answer(q) for q in sub_questions]
    if not sub_answers or any(answer.abstained for answer in sub_answers):
        return {"abstained": True, "sub_questions": sub_questions, "answer": None, "citations": []}
    citations = [c for answer in sub_answers for c in answer.citations]
    combined = " ".join(answer.text for answer in sub_answers)
    return {"abstained": False, "sub_questions": sub_questions, "answer": combined, "citations": citations}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("question")
    args = parser.parse_args()
    result = answer_multi_hop(args.question)
    if result["abstained"]:
        print("I can't find that in the documentation.")
    else:
        print(result["answer"])
        print("sources:", ", ".join(result["citations"]))


if __name__ == "__main__":
    main()
