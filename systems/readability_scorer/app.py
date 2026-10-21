"""Approximate Flesch-Kincaid reading grade level without NLP libraries.

Syllables are estimated by counting vowel-letter runs, which is a rough
proxy and will misjudge many real words.
"""
from __future__ import annotations

import argparse
import re

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_RE.split(text.strip()) if re.search(r"[A-Za-z]", s)]

_WORD = re.compile(r"[A-Za-z]+")
_VOWEL_GROUP = re.compile(r"[aeiouy]+")


def _syllables(word: str) -> int:
    word = word.lower()
    count = len(_VOWEL_GROUP.findall(word))
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def grade_level(text: str) -> float:
    words = _WORD.findall(text)
    sents = sentences(text) or [text]
    if not words:
        return 0.0
    syllables = sum(_syllables(w) for w in words)
    score = 0.39 * (len(words) / len(sents)) + 11.8 * (syllables / len(words)) - 15.59
    return round(score, 2)


def band(grade: float) -> str:
    if grade <= 6:
        return "simple"
    if grade <= 12:
        return "standard"
    return "complex"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("text")
    args = parser.parse_args()
    grade = grade_level(args.text)
    print(f"grade_level: {grade}")
    print(f"band: {band(grade)}")


if __name__ == "__main__":
    main()
