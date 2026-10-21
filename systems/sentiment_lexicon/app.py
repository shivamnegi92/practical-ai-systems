"""Lexicon-based positive/negative/neutral sentiment classifier.

No stemming or embeddings: each lexicon list spells out the inflections it
should match. Ties between positive and negative counts resolve to neutral.
"""
from __future__ import annotations

import argparse
import re

POSITIVE = {
    "good", "great", "excellent", "love", "loved", "loves", "happy",
    "amazing", "fantastic", "wonderful", "easy", "fast",
}
NEGATIVE = {
    "bad", "terrible", "hate", "hated", "hates", "slow", "broken",
    "awful", "horrible", "worst", "confusing", "frustrating",
}
_WORD = re.compile(r"[a-z]+")


def _words(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def classify(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError(f"text must be a str, got {type(text).__name__}")
    words = _words(text)
    positive = sum(w in POSITIVE for w in words)
    negative = sum(w in NEGATIVE for w in words)
    if positive > negative:
        return "positive"
    if negative > positive:
        return "negative"
    return "neutral"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("text")
    args = parser.parse_args()
    print(classify(args.text))


if __name__ == "__main__":
    main()
