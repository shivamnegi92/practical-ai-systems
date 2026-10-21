import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.sentiment_lexicon.app import classify

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    correct = [classify(c["text"]) == c["label"] for c in cases]
    return {
        "cases": len(cases),
        "accuracy": round(mean(correct), 4),
        "scope": "small hand-built lexicon; exact word match, no stemming, heuristic three-token negation window",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
