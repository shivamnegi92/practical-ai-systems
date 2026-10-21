"""Two-stage triage -> specialist handoff with escalation for low-confidence requests.

A triage step scores the request against fixed keyword sets per category.
Anything with zero keyword matches, or fewer matches than
`CONFIDENCE_THRESHOLD`, escalates to a human instead of being routed.
"""
from __future__ import annotations

import argparse

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

CATEGORIES = {
    "billing": {"invoice", "charge", "refund", "payment", "price"},
    "technical": {"error", "bug", "crash", "broken", "login"},
    "account": {"password", "delete", "username", "profile"},
}
CONFIDENCE_THRESHOLD = 2
SPECIALISTS = {
    "billing": lambda request: {"resolution": "routed to billing specialist"},
    "technical": lambda request: {"resolution": "routed to technical specialist"},
    "account": lambda request: {"resolution": "routed to account specialist"},
}


def triage(text: str) -> tuple[str | None, int]:
    tokens = set(tokenize(text))
    scores = {category: len(tokens & keywords) for category, keywords in CATEGORIES.items()}
    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]
    winners = [category for category, score in scores.items() if score == best_score]
    return (best_category if len(winners) == 1 else None, best_score) if best_score else (None, 0)


def handle(request: dict) -> dict:
    """Route a request to a specialist, or escalate when triage is unsure."""
    category, confidence = triage(request.get("text", ""))
    if category is None or confidence < CONFIDENCE_THRESHOLD:
        return {"status": "escalated", "category": category, "confidence": confidence}
    return {
        "status": "resolved",
        "category": category,
        "confidence": confidence,
        **SPECIALISTS[category](request),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("text")
    args = parser.parse_args()
    print(handle({"text": args.text}))


if __name__ == "__main__":
    main()
