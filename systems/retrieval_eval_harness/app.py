"""Compute recall@k, MRR, and nDCG@k for ranked retrieval, and compare two strategies.

Carries its own bundled BM25 index and synonym-expansion query rewriter
(see `systems/query_rewriter` for the original, standalone version of this
pattern) to show how retrieval-quality metrics move together (or don't)
when a retrieval strategy changes.

Standalone: zero imports outside the Python standard library.
"""
from __future__ import annotations

import math
import re
from collections import Counter

_STOPWORDS = frozenset(
    "a an and are as at be by can do does for from has have how i in is it its of on or "
    "our that the their this to was we what when where which who why will with you your".split()
)
_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _stem(token: str) -> str:
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 2 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def tokenize(text: str) -> list[str]:
    return [_stem(t) for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS]


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


SYNONYMS = {
    "price": ["cost"],
    "pricing": ["cost"],
    "terminate": ["cancel"],
    "unsubscribe": ["cancel"],
    "erase": ["delete"],
    "remove": ["delete"],
}


def expand_query(query: str) -> str:
    normalized = {stem: aliases for word, aliases in SYNONYMS.items() for stem in tokenize(word)}
    extra = [synonym for term in tokenize(query) for synonym in normalized.get(term, [])]
    return " ".join([query] + extra)


def recall_at_k(ranked_ids: list[str], relevant_ids: set[str], k: int) -> float:
    if not relevant_ids:
        return 0.0
    return len(set(ranked_ids[:k]) & relevant_ids) / len(relevant_ids)


def reciprocal_rank(ranked_ids: list[str], relevant_ids: set[str]) -> float:
    for rank, doc_id in enumerate(ranked_ids, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(ranked_ids: list[str], relevance: dict[str, int], k: int) -> float:
    dcg = sum(relevance.get(doc_id, 0) / math.log2(i + 1) for i, doc_id in enumerate(ranked_ids[:k], start=1))
    ideal = sorted(relevance.values(), reverse=True)[:k]
    idcg = sum(rel / math.log2(i + 1) for i, rel in enumerate(ideal, start=1))
    return dcg / idcg if idcg else 0.0


def evaluate_ranking(ranked_ids: list[str], relevance: dict[str, int], k: int = 3) -> dict:
    relevant_ids = {doc_id for doc_id, rel in relevance.items() if rel > 0}
    return {
        "recall_at_k": round(recall_at_k(ranked_ids, relevant_ids, k), 4),
        "mrr": round(reciprocal_rank(ranked_ids, relevant_ids), 4),
        "ndcg_at_k": round(ndcg_at_k(ranked_ids, relevance, k), 4),
    }


def compare_strategies(corpus: dict[str, str], queries: list[dict], k: int = 3) -> dict:
    """Score a baseline BM25 run against a synonym-expanded run on the same queries."""
    index = BM25(corpus)
    baseline_scores, expanded_scores = [], []
    for query in queries:
        relevance = query["relevance"]
        baseline_ranked = [doc_id for doc_id, _ in index.search(query["text"], k)]
        expanded_ranked = [doc_id for doc_id, _ in index.search(expand_query(query["text"]), k)]
        baseline_scores.append(evaluate_ranking(baseline_ranked, relevance, k))
        expanded_scores.append(evaluate_ranking(expanded_ranked, relevance, k))

    def avg(metric: str, scores: list[dict]) -> float:
        return round(sum(s[metric] for s in scores) / len(scores), 4) if scores else 0.0

    metrics = ("recall_at_k", "mrr", "ndcg_at_k")
    return {
        "baseline": {m: avg(m, baseline_scores) for m in metrics},
        "expanded": {m: avg(m, expanded_scores) for m in metrics},
    }
