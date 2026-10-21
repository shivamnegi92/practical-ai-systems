"""Two-sample canary vs. baseline guardrail check for a promote/rollback decision.

This is a fixed-threshold comparison, not a statistically rigorous A/B
test: it ignores sample size, variance, and confidence intervals. Use it
to illustrate the decision shape, not to gate a real rollout.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def decide(
    baseline: dict,
    canary: dict,
    max_error_rate_delta: float = 0.02,
    max_latency_regression_pct: float = 0.20,
) -> dict:
    for name, value in (("max_error_rate_delta", max_error_rate_delta), ("max_latency_regression_pct", max_latency_regression_pct)):
        try:
            valid = not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value) and value >= 0
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError(f"{name} must be a finite nonnegative number")
    error_delta = canary["error_rate"] - baseline["error_rate"]
    base_latency = baseline["p95_latency_ms"]
    latency_regression = (canary["p95_latency_ms"] - base_latency) / base_latency if base_latency else 0.0
    reasons = []
    if error_delta > max_error_rate_delta:
        reasons.append("error_rate_regression")
    if latency_regression > max_latency_regression_pct:
        reasons.append("latency_regression")
    return {
        "decision": "rollback" if reasons else "promote",
        "reasons": reasons,
        "error_rate_delta": round(error_delta, 4),
        "latency_regression_pct": round(latency_regression, 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("baseline_file", type=Path)
    parser.add_argument("canary_file", type=Path)
    args = parser.parse_args()
    baseline = json.loads(args.baseline_file.read_text())
    canary = json.loads(args.canary_file.read_text())
    print(json.dumps(decide(baseline, canary), indent=2))


if __name__ == "__main__":
    main()
