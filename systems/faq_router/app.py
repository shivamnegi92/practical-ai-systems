"""Route a support message to an intent using keyword-overlap scoring."""
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
            token = token[: -len(suffix)]
            break
    return token[:-1] if len(token) > 3 and token.endswith("e") else token


def tokenize(text: str) -> list[str]:
    return [_stem(t) for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS]

INTENTS = {
    "greeting": {"hi", "hello", "hey", "greetings"},
    "goodbye": {"bye", "goodbye", "farewell", "thanks", "thank"},
    "billing_question": {"invoice", "charge", "bill", "billing", "payment", "refund", "price"},
    "cancel_request": {"cancel", "unsubscribe", "terminate", "close"},
    "technical_issue": {"error", "bug", "crash", "broken", "not", "working", "fail", "log in"},
}
FALLBACK = "unknown"


def route(text: str) -> str:
    """Score each intent by keyword overlap; first-seen intent wins ties."""
    tokens = set(tokenize(text))
    phrase_tokens = [_stem(t) for t in _TOKEN_RE.findall(text.lower())]
    best_intent, best_score = FALLBACK, 0
    for intent, keywords in INTENTS.items():
        normalized = {tuple(_stem(t) for t in _TOKEN_RE.findall(keyword)) for keyword in keywords}
        score = sum(
            keyword[0] in tokens if len(keyword) == 1 else any(
                tuple(phrase_tokens[index:index + len(keyword)]) == keyword
                for index in range(len(phrase_tokens) - len(keyword) + 1)
            )
            for keyword in normalized
        )
        if score > best_score:
            best_intent, best_score = intent, score
    return best_intent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("text")
    args = parser.parse_args()
    print(route(args.text))


if __name__ == "__main__":
    main()
