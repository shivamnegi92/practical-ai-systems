"""Heuristic scanner for likely prompt-injection patterns in untrusted text.

Intended use: scan retrieved documents or tool outputs before they are
inserted into a model prompt. This is pattern matching, not a classifier
trained on real attack traffic -- treat it as one weak signal among several
defenses, not a guarantee of safety.
"""
from __future__ import annotations

import argparse
import re

PATTERNS = [
    ("override_instructions", re.compile(r"ignore\b.{0,30}\b(?:instructions|rules|prompt)", re.I | re.S)),
    ("reveal_prompt", re.compile(r"(?:reveal|print|show|tell).{0,20}(?:system prompt|instructions)", re.I | re.S)),
    ("role_override", re.compile(r"you are now\b|act as\b.{0,30}(?:unrestricted|jailbroken|dan)", re.I | re.S)),
    ("disregard_safety", re.compile(r"disregard.{0,20}(?:safety|policy|guidelines)", re.I | re.S)),
    ("suspicious_encoding", re.compile(r"\b[A-Za-z0-9+/]{40,}={0,2}\b")),
]


def scan(text: str) -> dict:
    matches = [
        {"pattern": name, "match": match.group()}
        for name, pattern in PATTERNS
        for match in pattern.finditer(text)
    ]
    return {"flagged": bool(matches), "matches": matches}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("text")
    args = parser.parse_args()
    result = scan(args.text)
    print("FLAGGED" if result["flagged"] else "clean")
    for match in result["matches"]:
        print(f"- {match['pattern']}: {match['match']}")


if __name__ == "__main__":
    main()
