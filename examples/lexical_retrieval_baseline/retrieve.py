"""A tiny, inspectable lexical retrieval baseline with no third-party dependencies."""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Mapping

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase and tokenize simple Latin-script words/numbers."""
    return TOKEN_PATTERN.findall(text.lower())


def rank_documents(query: str, documents: Mapping[str, str], top_k: int = 5) -> list[tuple[str, float]]:
    """Rank documents by query-term overlap normalized by query length.

    This deliberately simple baseline uses unique query tokens and raw term
    overlap. It is useful for debugging and comparison, not semantic search.
    Ties are broken by document ID for deterministic output.
    """
    if top_k < 1:
        raise ValueError("top_k must be at least 1")

    query_tokens = set(tokenize(query))
    if not query_tokens:
        return []

    scored: list[tuple[str, float]] = []
    for document_id, text in documents.items():
        document_tokens = set(tokenize(text))
        overlap = len(query_tokens & document_tokens)
        if overlap:
            scored.append((document_id, overlap / len(query_tokens)))

    scored.sort(key=lambda item: (-item[1], item[0]))
    return scored[:top_k]
