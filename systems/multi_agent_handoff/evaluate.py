import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.multi_agent_handoff.app import handle

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    correct = [handle({"text": c["text"]})["status"] == c["gold_status"] for c in cases]
    return {
        "cases": len(cases),
        "handoff_accuracy": round(mean(correct), 4),
        "routing_accuracy": round(mean(handle({"text": c["text"]})["status"] == c["gold_status"] and handle({"text": c["text"]})["category"] == c["gold_category"] for c in cases), 4),
        "scope": "fixed keyword-overlap triage over three categories; escalation threshold is a hand-picked constant",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
