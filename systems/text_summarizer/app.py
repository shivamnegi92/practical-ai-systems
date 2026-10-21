"""Extractive summarizer: rank sentences by shared frequent-word score."""
from __future__ import annotations

import argparse
import re
from collections import Counter

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


def summarize(text: str, n: int = 2) -> list[str]:
    """Pick the n highest-scoring sentences, kept in original order."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError('n must be a nonnegative integer')
    sents = sentences(text)
    if len(sents) <= n:
        return sents
    freq = Counter(tokenize(text))
    scored = []
    for index, sent in enumerate(sents):
        terms = tokenize(sent)
        score = sum(freq[t] for t in terms) / len(terms) if terms else 0.0
        scored.append((score, index, sent))
    top = sorted(scored, key=lambda row: -row[0])[:n]
    return [sent for _, _, sent in sorted(top, key=lambda row: row[1])]


def compression_ratio(text: str, summary: list[str]) -> float:
    original = len(text)
    compressed = len(" ".join(summary))
    return compressed / original if original else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("text")
    parser.add_argument("--n", type=int, default=2)
    args = parser.parse_args()
    summary = summarize(args.text, args.n)
    print("\n".join(summary))
    print(f"compression_ratio: {compression_ratio(args.text, summary):.2f}")


if __name__ == "__main__":
    main()
