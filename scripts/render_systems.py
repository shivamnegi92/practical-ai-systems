"""Render the learner-oriented index of runnable system examples."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.registry import load_manifests  # noqa: E402

SYSTEMS = load_manifests()
START = "<!-- SYSTEMS:START -->"
END = "<!-- SYSTEMS:END -->"
LEVEL_SUMMARIES = {
    "Beginner": "Start here if this is your first AI project. No model account or paid API key is needed.",
    "Intermediate": "For people comfortable with basic Python who want to work with data and evaluation metrics.",
    "Advanced": "For builders ready to reason about agent boundaries, protocols, and evaluation quality.",
}


def _packet(root: Path, name: str) -> tuple[int, dict]:
    folder = root / "systems" / name
    for file in ("README.md", "evaluate.py", "eval/results.json"):
        if not (folder / file).exists():
            raise ValueError(f"{name}: missing {file}")
    record = json.loads((folder / "eval/results.json").read_text())
    if record.get("system") != name or not record.get("method"):
        raise ValueError(f"{name}: malformed result record")
    count = record.get("dataset", {}).get("cases")
    metrics = record.get("metrics", {})
    if not isinstance(count, int) or count < 1 or not metrics:
        raise ValueError(f"{name}: missing case count or metrics")
    return count, metrics


def render_readme(readme: str, root: Path = ROOT) -> str:
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one systems marker pair")
    start = readme.index(START)
    end = readme.index(END)
    if end < start:
        raise ValueError("README systems markers are out of order")

    systems = load_manifests(root)
    counts = {level: sum(entry["level"] == level for entry in systems.values()) for level in LEVEL_SUMMARIES}
    lines = [
        "",
        "Choose a level that feels right. You can skip ahead if you already know the basics.",
        "",
        f"- **[Beginner](#beginner)** — {counts['Beginner']} first projects; no model setup.",
        f"- **[Intermediate](#intermediate)** — {counts['Intermediate']} projects; Python and basic metrics help.",
        f"- **[Advanced](#advanced)** — {counts['Advanced']} projects; system boundaries and evaluation.",
        "",
    ]

    for level, summary in LEVEL_SUMMARIES.items():
        lines.extend([f"### {level}", "", summary, ""])
        for name, info in systems.items():
            if info["level"] != level:
                continue
            count, metrics = _packet(root, name)
            readme_path = f"systems/{name}/README.md"
            result_path = f"systems/{name}/eval/results.json"
            lines.extend([
                f"#### [{info['title']}]({readme_path})",
                "",
                info["hook"],
                "",
                f"**Before you start:** {info['prerequisites']}",
                "",
                f"**Try this:** run the project README quickstart, then its test and evaluator.",
                f"[Evaluation results and cases]({result_path}) · {count} small synthetic cases. Scores are learning fixtures, not production benchmarks.",
                "",
            ])

    new_readme = readme[:start] + START + "\n" + "\n".join(lines) + END + readme[end + len(END):]
    return new_readme


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    path = args.root / "README.md"
    current = path.read_text(encoding="utf-8")
    try:
        rendered = render_readme(current, args.root)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"Experience-level index validation failed: {exc}", file=sys.stderr)
        return 1
    if args.write:
        path.write_text(rendered, encoding="utf-8")
        print(f"Rendered {len(SYSTEMS)} projects in beginner/intermediate/advanced levels.")
    elif rendered != current:
        print("README experience-level section is stale; run python scripts/render_systems.py --write", file=sys.stderr)
        return 1
    else:
        print(f"Validated {len(SYSTEMS)} projects in the learning-level index.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
