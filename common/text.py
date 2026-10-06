"""Tiny, dependency-free text utilities shared by systems."""
from __future__ import annotations

import math
import re
from collections import Counter

STOPWORDS = frozenset(
    "a an and are as at be by can do does for from has have how i in is it its of on or "
    "our that the their this to was we what when where which who why will with you your".split()
)
_TOKEN = re.compile(r"[a-z0-9]+")
_SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _stem(token: str) -> str:
    """Very light suffix stripping so 'refunds' matches 'refund'."""
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
