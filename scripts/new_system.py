"""Scaffold a new standalone system that already passes every repository check.

Usage:
    python3 scripts/new_system.py my_system --title "My system" --level Beginner \\
        --hook "One sentence on what learners build." --prerequisites "Basic Python."

Then replace the placeholder logic, cases, and tests with your real system.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_systems import NAME_RE  # noqa: E402
from scripts.registry import LEVELS, load_manifests  # noqa: E402

TEMPLATE_DIR = ROOT / "templates" / "system"


def render(text: str, values: dict[str, str]) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda match: values.get(match.group(1), match.group(0)), text)


def scaffold(name: str, title: str, level: str, hook: str, prerequisites: str, root: Path = ROOT) -> Path:
    if not NAME_RE.match(name):
        raise ValueError("name must be snake_case, e.g. 'keyword_extractor'")
    if level not in LEVELS:
        raise ValueError(f"level must be one of {', '.join(LEVELS)}")
    target = root / "systems" / name
    if target.exists():
        raise ValueError(f"systems/{name} already exists")
    same_level = [m["order"] for m in load_manifests(root).values() if m["level"] == level]
    values = {
        "name": name,
        "title": title,
        "kebab": name.replace("_", "-"),
        "title_class": "".join(part.capitalize() for part in name.split("_")),
        "hook": hook,
    }
    for src in TEMPLATE_DIR.rglob("*"):
        if src.is_dir():
            continue
        rel = Path(render(str(src.relative_to(TEMPLATE_DIR)), values).removesuffix(".tmpl"))
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        content_values = dict(values)
        for key in ("title", "hook"):
            value = content_values[key]
            if dest.suffix == ".html":
                value = html.escape(value)
            elif dest.suffix == ".py":
                value = value.encode("unicode_escape").decode("ascii").replace('"""', '\\"\\"\\"')
            elif dest.suffix == ".ts":
                value = " ".join(value.splitlines())
            content_values[key] = value
        dest.write_text(render(src.read_text(encoding="utf-8"), content_values), encoding="utf-8")
    manifest = {"title": title, "level": level, "order": max(same_level, default=0) + 1,
                "prerequisites": prerequisites, "hook": hook}
    (target / "system.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name", help="snake_case folder name under systems/")
    parser.add_argument("--title", required=True)
    parser.add_argument("--level", required=True, choices=LEVELS)
    parser.add_argument("--hook", required=True, help="one-sentence learner-facing summary")
    parser.add_argument("--prerequisites", required=True)
    args = parser.parse_args()
    try:
        target = scaffold(args.name, args.title, args.level, args.hook, args.prerequisites)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    rel = target.relative_to(ROOT)
    print(f"Created {rel}. Next steps:")
    print(f"  1. Implement {rel}/app.py and replace eval/cases.json with real synthetic cases.")
    print(f"  2. python3 -m unittest discover -s {rel} -t . -v")
    print(f"  3. python3 scripts/evaluate_systems.py --check --write --only {args.name}")
    print(f"  4. python3 scripts/render_systems.py --write && python3 scripts/check_systems.py")
    print(f"  5. cd {rel}/web && npm ci && npm test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
