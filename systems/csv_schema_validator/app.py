"""Validate rows of structured data against a small declared schema.

Catches missing required fields and obvious type mismatches before bad
rows reach a downstream extraction or indexing pipeline.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

TYPE_MAP = {"string": str, "number": (int, float), "boolean": bool}


def validate_row(schema: dict, row: dict) -> list[str]:
    errors = []
    for field, spec in schema.items():
        required = spec.get("required", False)
        expected_type = TYPE_MAP.get(spec.get("type", "string"), str)
        value = row.get(field)
        if value in (None, ""):
            if required:
                errors.append(f"missing:{field}")
            continue
        if not isinstance(value, expected_type) or (spec.get("type") == "number" and isinstance(value, float) and not math.isfinite(value)):
            errors.append(f"type:{field}")
    return errors


def validate_rows(schema: dict, rows: list[dict]) -> list[dict]:
    return [{"row": i, "errors": validate_row(schema, row)} for i, row in enumerate(rows)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("schema_file", type=Path)
    parser.add_argument("rows_file", type=Path)
    args = parser.parse_args()
    schema = json.loads(args.schema_file.read_text())
    rows = json.loads(args.rows_file.read_text())
    print(json.dumps(validate_rows(schema, rows), indent=2))


if __name__ == "__main__":
    main()
