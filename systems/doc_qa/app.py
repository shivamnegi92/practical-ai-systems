"""Document Q&A with citations and abstention.

Baseline: BM25 retrieval over paragraph chunks + extractive answer (best
matching sentence). Optional model mode (PAS_LLM) writes the answer from the
retrieved chunks only and must cite a retrieved chunk id, or we abstain.
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path

from common.llm import LLM, from_env
from common.text import BM25, sentences, tokenize

DATA_DIR = Path(__file__).parent / "data"
ABSTAIN = "I can't find that in the documentation."
PROMPT = """Answer the question using ONLY the context. Cite the chunk id in square brackets, e.g. [billing.md#1].
If the context does not contain the answer, reply exactly: {abstain}

Context:
{context}

Question: {question}
Answer:"""


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
