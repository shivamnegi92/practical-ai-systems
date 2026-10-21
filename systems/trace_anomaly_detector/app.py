"""Flag anomalous trace durations using z-scores against a historical baseline.

A trace is flagged when it carries an explicit error flag, or when its
duration is more than `z_threshold` standard deviations from the baseline
mean. This is a simple statistical heuristic, not a trained anomaly model.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def _stdev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return variance**0.5


def _valid_measurement(value) -> bool:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value) and value >= 0
    except OverflowError:
        return False


def detect_anomalies(baseline: list[float], traces: list[dict], z_threshold: float = 3.0) -> list[dict]:
    if not _valid_measurement(z_threshold):
        raise ValueError('z threshold must be finite and nonnegative')
    if not all(_valid_measurement(value) for value in baseline):
        raise ValueError('baseline durations must be finite and nonnegative')
    if not all(_valid_measurement(trace['duration_ms']) for trace in traces):
        raise ValueError('trace duration must be finite and nonnegative')
    baseline_mean, baseline_sd = mean(baseline), _stdev(baseline)
    results = []
    for trace in traces:
        duration = trace["duration_ms"]
        z = (duration - baseline_mean) / baseline_sd if baseline_sd else 0.0
        anomalous = bool(trace.get("error", False)) or abs(z) > z_threshold
        results.append({"name": trace["name"], "z_score": round(z, 2), "anomalous": anomalous})
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("baseline_file", type=Path)
    parser.add_argument("traces_file", type=Path)
    args = parser.parse_args()
    baseline = json.loads(args.baseline_file.read_text())
    traces = json.loads(args.traces_file.read_text())
    print(json.dumps(detect_anomalies(baseline, traces), indent=2))


if __name__ == "__main__":
    main()
