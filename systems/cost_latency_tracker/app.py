"""Summarize a request log into latency percentiles, cost, and budget breaches."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

def percentile(values, pct: float) -> float:
    if not isinstance(pct, (int, float)) or isinstance(pct, bool) or not (0.0 <= pct <= 100.0):
        raise ValueError(f"pct must be between 0.0 and 100.0, got {pct!r}")
    ordered = sorted(values)
    if not ordered:
        return 0.0
    pos = (len(ordered) - 1) * pct / 100
    lo, hi = int(pos), min(int(pos) + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)


def summarize(requests: list[dict]) -> dict:
    latencies = [r["latency_ms"] for r in requests]
    total_cost = sum(r["cost_usd"] for r in requests)
    tokens = sum(r.get("tokens", 0) for r in requests)
    return {
        "requests": len(requests),
        "p50_latency_ms": round(percentile(latencies, 50), 2),
        "p95_latency_ms": round(percentile(latencies, 95), 2),
        "total_cost_usd": round(total_cost, 4),
        "cost_per_1k_tokens_usd": round(total_cost / tokens * 1000, 4) if tokens else 0.0,
    }


def check_budget(summary: dict, max_p95_latency_ms: float, max_cost_usd: float) -> dict:
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
