"""Summarize a request log into latency percentiles, cost, and budget breaches."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def _measurement(value, name: str, integer: bool = False):
    valid = isinstance(value, (int, float)) and not isinstance(value, bool)
    try:
        valid = valid and math.isfinite(value) and value >= 0
    except OverflowError:
        valid = False
    if not valid or (integer and value != int(value)):
        raise ValueError(f"{name} must be a finite nonnegative {'integer' if integer else 'number'}")
    return value

def percentile(values, pct: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    pos = (len(ordered) - 1) * pct / 100
    lo, hi = int(pos), min(int(pos) + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def summarize(requests: list[dict]) -> dict:
    for i, request in enumerate(requests):
        for field in ("latency_ms", "cost_usd", "tokens"):
            _measurement(request.get(field, 0) if field == "tokens" else request[field],
                         f"requests[{i}].{field}", integer=field == "tokens")
    latencies = [r["latency_ms"] for r in requests]
    total_cost = sum(r["cost_usd"] for r in requests)
    tokens = sum(r.get("tokens", 0) for r in requests)
    summary = {
        "requests": len(requests),
        "p50_latency_ms": round(percentile(latencies, 50), 2),
        "p95_latency_ms": round(percentile(latencies, 95), 2),
        "total_cost_usd": round(total_cost, 4),
        "cost_per_1k_tokens_usd": round(total_cost / tokens * 1000, 4) if tokens else 0.0,
    }
    for field, value in summary.items():
        _measurement(value, field)
    return summary


def check_budget(summary: dict, max_p95_latency_ms: float, max_cost_usd: float) -> dict:
    _measurement(summary["p95_latency_ms"], "p95_latency_ms")
    _measurement(summary["total_cost_usd"], "total_cost_usd")
    _measurement(max_p95_latency_ms, "max_p95_latency_ms")
    _measurement(max_cost_usd, "max_cost_usd")
    reasons = []
    if summary["p95_latency_ms"] > max_p95_latency_ms:
        reasons.append("latency")
    if summary["total_cost_usd"] > max_cost_usd:
        reasons.append("cost")
    return {"breached": bool(reasons), "reasons": reasons}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("log_file", type=Path)
    args = parser.parse_args()
    requests = json.loads(args.log_file.read_text())
    print(json.dumps(summarize(requests), indent=2))


if __name__ == "__main__":
    main()
