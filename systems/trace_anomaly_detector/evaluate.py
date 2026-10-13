import json
from pathlib import Path

def prf(tp: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
from systems.trace_anomaly_detector.app import detect_anomalies

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    case = json.loads((EVAL_DIR / "cases.json").read_text())
    tp = fp = fn = 0
    count = 0
    for scenario in [case, *case.get('scenarios', [])]:
        results = detect_anomalies(scenario["baseline"], scenario["traces"])
        count += len(results)
        for result, gold in zip(results, scenario["gold_anomalous"]):
            tp += result["anomalous"] and gold
            fp += result["anomalous"] and not gold
            fn += (not result["anomalous"]) and gold
    metrics = prf(tp, fp, fn)
    return {
        "cases": count,
        **{k: round(v, 4) for k, v in metrics.items()},
        "scope": "synthetic variable, constant and zero-mean baselines; z-score with a strict 50% constant-baseline tolerance; not a trained anomaly model",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
