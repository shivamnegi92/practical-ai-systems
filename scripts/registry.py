"""Discover runnable systems from per-folder ``system.json`` manifests.

Each system owns its metadata, so adding a system never requires editing a
central list (no merge conflicts between unrelated contributions).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("Beginner", "Intermediate", "Advanced")
REQUIRED_KEYS = ("title", "level", "order", "prerequisites", "hook")


def load_manifests(root: Path = ROOT) -> dict[str, dict]:
    """Return {system_name: manifest} sorted by level, then order, then name."""
    manifests = {}
    for path in (root / "systems").glob("*/system.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"{path.parent.name}: system.json must be an object")
        missing = [key for key in REQUIRED_KEYS if key not in data]
        if missing:
            raise ValueError(f"{path.parent.name}: system.json missing {', '.join(missing)}")
        if data["level"] not in LEVELS:
            raise ValueError(f"{path.parent.name}: level must be one of {', '.join(LEVELS)}")
        for field in ("title", "hook", "prerequisites"):
            if not isinstance(data[field], str) or not data[field].strip():
                raise ValueError(f"{path.parent.name}: {field} must be a non-empty string")
        order = data["order"]
        if isinstance(order, bool) or not isinstance(order, (int, float)) or (isinstance(order, float) and not math.isfinite(order)):
            raise ValueError(f"{path.parent.name}: order must be a finite number")
        manifests[path.parent.name] = data
    return dict(sorted(manifests.items(), key=lambda kv: (LEVELS.index(kv[1]["level"]), kv[1]["order"], kv[0])))
