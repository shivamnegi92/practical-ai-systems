"""Two-sample canary guardrail check for a promote/rollback/hold decision.

This is a fixed-threshold comparison, not a statistically rigorous A/B
test: it ignores sample size, variance, and confidence intervals. Use it
to illustrate the decision shape, not to gate a real rollout.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def decide(
    baseline: dict,
    canary: dict,
    max_error_rate_delta: float = 0.02,
    max_latency_regression_pct: float = 0.20,
) -> dict:
    error_delta = canary["error_rate"] - baseline["error_rate"]
    base_latency = baseline.get("p95_latency_ms")
    latency_regression = (canary["p95_latency_ms"] - base_latency) / base_latency if base_latency is not None and base_latency > 0 else None
    reasons = []
    if error_delta > max_error_rate_delta:
        reasons.append("error_rate_regression")
    if latency_regression is not None and latency_regression > max_latency_regression_pct:
        reasons.append("latency_regression")
    decision = "rollback" if reasons else "hold" if latency_regression is None else "promote"
    if latency_regression is None:
        reasons.append("missing_latency_baseline")
    return {
        "decision": decision,
        "reasons": reasons,
        "error_rate_delta": round(error_delta, 4),
        "latency_regression_pct": round(latency_regression, 4) if latency_regression is not None else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("baseline_file", type=Path)
    parser.add_argument("canary_file", type=Path)
    args = parser.parse_args()
    baseline = json.loads(args.baseline_file.read_text(encoding="utf-8"))
    canary = json.loads(args.canary_file.read_text(encoding="utf-8"))
    print(json.dumps(decide(baseline, canary), indent=2))


if __name__ == "__main__":
    main()
