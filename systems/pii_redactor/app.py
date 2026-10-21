"""Detect and redact a small set of obvious PII patterns in text.

This is pattern matching, not an entity-recognition model and not a
compliance tool. It will miss anything that does not match the regexes
below and may false-positive on lookalike strings.
"""
from __future__ import annotations

import argparse
import re

PATTERNS = {
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "phone": re.compile(r"(?<!\w)(?:\+?1[-.\s]?)?(?:\(\d{3}\)\s?|\d{3}[-.\s])\d{3}[-.\s]\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b(?:(?:\d{4}[-\s]){3}\d{4}|\d{16})\b"),
}


def detect(text: str) -> list[dict]:
    findings = [
        {"type": label, "match": match.group(), "start": match.start(), "end": match.end()}
        for label, pattern in PATTERNS.items()
        for match in pattern.finditer(text)
    ]
    return sorted(findings, key=lambda f: f["start"])


def redact(text: str) -> str:
    for finding in sorted(detect(text), key=lambda f: -f["start"]):
        tag = f"[REDACTED:{finding['type'].upper()}]"
        text = text[: finding["start"]] + tag + text[finding["end"] :]
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("text")
    args = parser.parse_args()
    print(redact(args.text))


if __name__ == "__main__":
    main()
