"""Detect near-duplicate questions using token Jaccard similarity."""
from __future__ import annotations

import argparse
from itertools import combinations

import re

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


def similarity(a: str, b: str) -> float:
    ta, tb = set(tokenize(a)), set(tokenize(b))
    if not ta and not tb:
        # Stopword-only questions carry no content tokens; only exact word matches are duplicates.
        return 1.0 if _TOKEN_RE.findall(a.lower()) == _TOKEN_RE.findall(b.lower()) else 0.0
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def find_duplicates(questions: list[str], threshold: float = 0.6) -> list[tuple[int, int, float]]:
    """Return (i, j, score) for every pair at or above the similarity threshold."""
    pairs = []
    for i, j in combinations(range(len(questions)), 2):
        score = similarity(questions[i], questions[j])
        if score >= threshold:
            pairs.append((i, j, round(score, 4)))
    return pairs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("question_a")
    parser.add_argument("question_b")
    parser.add_argument("--threshold", type=float, default=0.6)
    args = parser.parse_args()
    score = similarity(args.question_a, args.question_b)
    print(f"similarity: {score:.2f}")
    print("duplicate" if score >= args.threshold else "not duplicate")


if __name__ == "__main__":
    main()
