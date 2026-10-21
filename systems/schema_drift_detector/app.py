"""Detect new fields, missing required fields, and type changes against a declared schema.

Useful for catching upstream data drift before it silently breaks a
downstream extraction or indexing pipeline.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def infer_type(value) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if value is None:
        return "null"
    return type(value).__name__


def detect_drift(schema: dict, records: list[dict]) -> dict:
    known_fields = set(schema)
    required = {field for field, spec in schema.items() if spec.get("required")}
    new_fields: set[str] = set()
    missing_required: set[str] = set()
    type_mismatches: set[str] = set()
    for record in records:
        new_fields |= set(record) - known_fields
        present = {k for k, v in record.items() if v not in (None, "")}
        missing_required |= required - present
        for field, value in record.items():
            if field in schema and value not in (None, "") and (infer_type(value) != schema[field]["type"] or (isinstance(value, float) and not math.isfinite(value))):
                type_mismatches.add(field)
    return {
        "new_fields": sorted(new_fields),
        "missing_required_fields": sorted(missing_required),
        "type_mismatched_fields": sorted(type_mismatches),
        "drift_detected": bool(new_fields or missing_required or type_mismatches),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("schema_file", type=Path)
    parser.add_argument("records_file", type=Path)
    args = parser.parse_args()
    schema = json.loads(args.schema_file.read_text())
    records = json.loads(args.records_file.read_text())
    print(json.dumps(detect_drift(schema, records), indent=2))


if __name__ == "__main__":
    main()
