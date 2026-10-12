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
_WORD = re.compile(r"[a-z]*n't|[a-z]+")
NEGATORS = {"not", "never", "no", "n't"}


def _words(text: str) -> list[str]:
    return _WORD.findall(text.lower().replace("\u2019", "'"))


def classify(text: str) -> str:
    words = _words(text)
    score = 0
    for index, word in enumerate(words):
        polarity = int(word in POSITIVE) - int(word in NEGATIVE)
        negated = any(token in NEGATORS or token.endswith("n't")
                      for token in words[max(0, index - 3):index])
        score += -polarity if negated else polarity
    if score > 0:
        return "positive"
    if score < 0:
        return "negative"
    return "neutral"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("text")
    args = parser.parse_args()
    print(classify(args.text))


if __name__ == "__main__":
    main()
