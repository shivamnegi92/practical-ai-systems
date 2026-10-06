"""Metric helpers and a single results.json format for every system."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def prf(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def percentile(values, pct: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    pos = (len(ordered) - 1) * pct / 100
    lo, hi = int(pos), min(int(pos) + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def cohen_kappa(a: list, b: list) -> float:
    """Agreement between two raters beyond chance."""
    if len(a) != len(b) or not a:
        raise ValueError("raters must label the same non-empty set")
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[label] * cb[label] for label in ca) / (n * n)
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


def write_results(path: Path, system: str, method: str, metrics: dict, cases: int, notes: str = "") -> dict:
    """Write results.json with rounded, sorted metrics so diffs stay readable."""
    record = {
        "system": system,
        "method": method,
        "dataset": {"cases": cases, "source": "synthetic, committed in eval/"},
        "metrics": {k: round(v, 4) if isinstance(v, float) else v for k, v in sorted(metrics.items())},
        "notes": notes,
    }
    Path(path).write_text(json.dumps(record, indent=2) + "\n")
    return record
