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
    "Beginner": "Start with offline examples and the core building blocks of AI systems.",
    "Intermediate": "Combine components and measure trade-offs across common AI workflows.",
    "Advanced": "Explore authorization, orchestration, evaluation quality, and operations.",
}


def _compact(text: str, limit: int = 72) -> str:
    """Keep descriptions scannable; the full hook remains in the system guide."""
    text = text.strip().rstrip(".")
    if len(text) > limit:
        text = text[:limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:") + "…"
    return text


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

    lines = [
        "",
        "Browse all 30 projects by increasing scope. You can skip ahead if you already know the basics.",
        "",
        "- **[Beginner](#beginner)** — no model setup; build core concepts.",
        "- **[Intermediate](#intermediate)** — combine components and measure trade-offs.",
        "- **[Advanced](#advanced)** — work through system boundaries and operations.",
        "",
    ]

    for level, summary in LEVEL_SUMMARIES.items():
        lines.extend([
            f"### {level}",
            "",
            "A compact directory of projects by level. Read a system guide for its focus and prerequisites.",
            "",
            "| System | Eval cases |",
            "|:--|--:|",
        ])
        for name, info in SYSTEMS.items():
            if info["level"] != level:
                continue
            count, _metrics = _packet(root, name)
            readme_path = f"systems/{name}/README.md"
            result_path = f"systems/{name}/eval/results.json"
            lines.append(
                f"| [{info['title']}]({readme_path}) | [{count}]({result_path}) |"
            )
        lines.append("")

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
