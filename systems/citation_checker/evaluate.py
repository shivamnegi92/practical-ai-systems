import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.citation_checker.app import check_citations

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    case = json.loads((EVAL_DIR / "cases.json").read_text())
    correct = []
    for scenario in [case, *case.get('scenarios', [])]:
        report = check_citations(scenario["answer"], scenario["chunks"])
        statuses = [r["status"] for r in report["results"]]
        correct.extend(got == gold for got, gold in zip(statuses, scenario["gold_statuses"]))
    return {
        "cases": len(correct),
        "citation_status_accuracy": round(mean(correct), 4),
        "scope": "lexical overlap plus literal numeric-token presence across eight synthetic citations; not semantic entailment",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
