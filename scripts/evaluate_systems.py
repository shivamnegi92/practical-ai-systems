"""Run all system evaluations and write comparable result records."""
from __future__ import annotations

import argparse
import importlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.registry import load_manifests  # noqa: E402

SYSTEMS = tuple(load_manifests())
COUNT_FIELDS = ("cases", "calls", "documents", "entries")


def normalize(name: str, raw: dict) -> dict:
    """Convert per-system outputs to a consistent evidence packet."""
    count_key = next((key for key in COUNT_FIELDS if key in raw), None)
    if count_key is None:
        raise ValueError(f"{name}: evaluation must report its workload size")
    if "metrics" in raw:
        metrics = raw["metrics"]
        count = raw.get("dataset", {}).get("cases", raw[count_key])
    else:
        metadata = set(COUNT_FIELDS) | {
            "method", "dataset", "scope", "note", "notes", "warning",
        }
        metrics = {
            key: value for key, value in raw.items()
            if key not in metadata and isinstance(value, (int, float))
        }
        count = raw[count_key]
    notes = [raw[key] for key in ("scope", "note", "notes", "warning") if raw.get(key)]
    return {
        "system": name,
        "method": raw.get("method", "deterministic evaluation on synthetic fixtures"),
        "dataset": {"cases": count, "source": "synthetic fixtures committed with system"},
        "metrics": dict(sorted(metrics.items())),
        "notes": " ".join(notes),
    }


def run_all(names: tuple[str, ...] = SYSTEMS) -> dict[str, dict]:
    results = {}
    for name in names:
        module = importlib.import_module(f"systems.{name}.evaluate")
        results[name] = normalize(name, module.evaluate())
    return results


def validate(results: dict[str, dict], expected: tuple[str, ...] = SYSTEMS) -> list[str]:
    errors = []
    if set(results) != set(expected):
        errors.append("system evaluation set does not match the declared systems")
    for name, result in results.items():
        dataset = result.get("dataset", {})
        if isinstance(dataset.get("cases"), bool) or not isinstance(dataset.get("cases"), int) or dataset["cases"] <= 0:
            errors.append(f"{name}: invalid case count")
        if not result.get("system") or not result.get("method"):
            errors.append(f"{name}: missing system/method metadata")
        metrics = result.get("metrics")
        if not isinstance(metrics, dict) or not metrics:
            errors.append(f"{name}: no metrics reported")
        else:
            for metric, value in metrics.items():
                if not isinstance(value, (int, float)) or (isinstance(value, float) and not math.isfinite(value)):
                    errors.append(f"{name}: {metric} must be a finite numeric metric")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate result packets")
    parser.add_argument("--write", action="store_true", help="write normalized eval/results.json packets")
    parser.add_argument("--only", help="evaluate a single system by folder name")
    args = parser.parse_args()
    if args.only and args.only not in SYSTEMS:
        print(f"unknown system: {args.only}", file=sys.stderr)
        return 1
    selected = (args.only,) if args.only else SYSTEMS
    results = run_all(selected)
    errors = validate(results, selected) if args.check else []
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    for name, result in results.items():
        print(f"{name}: {json.dumps(result, sort_keys=True)}")
        if args.write:
            path = ROOT / "systems" / name / "eval" / "results.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
