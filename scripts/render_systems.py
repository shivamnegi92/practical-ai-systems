"""Render the learner-oriented index of runnable system examples."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEMS = {
    "doc_qa": {"title": "Document Q&A with citations", "level": "Beginner", "prerequisites": "Terminal basics; Python is optional to run it.", "hook": "Find a source paragraph, answer from its evidence, cite it, or abstain."},
    "invoice_extract": {"title": "Invoice field extraction", "level": "Beginner", "prerequisites": "Basic Python and key/value data.", "hook": "Extract invoice fields, then validate dates and arithmetic."},
    "repo_guard": {"title": "Repository hygiene checks", "level": "Beginner", "prerequisites": "Basic file and folder navigation.", "hook": "Run simple local checks and see why toy patterns miss real risks."},
    "multimodal_ocr": {"title": "Post-OCR document extraction", "level": "Intermediate", "prerequisites": "Basic Python and JSON/list/dictionary data.", "hook": "Normalize OCR line order from bounding boxes, then extract fields. OCR itself is not run."},
    "entity_extraction": {"title": "Entity spans and error analysis", "level": "Intermediate", "prerequisites": "Python functions, regular expressions, and basic metrics.", "hook": "Extract person/date/money spans and inspect exact-match precision, recall, and F1."},
    "semantic_cache": {"title": "Exact-response cache", "level": "Intermediate", "prerequisites": "Python classes, dictionaries, and basic cache concepts.", "hook": "Explore normalized keys, TTL expiry, LRU eviction, and model/version isolation."},
    "voice_eval": {"title": "Voice-agent transcript evaluator", "level": "Advanced", "prerequisites": "Structured transcripts and evaluation rubrics.", "hook": "Score call success, forbidden actions, and latency separately."},
    "judge_audit": {"title": "Judge agreement audit", "level": "Advanced", "prerequisites": "Classification metrics and labeled data.", "hook": "Compare a heuristic with human ratings and inspect rater disagreement."},
    "bounded_agent": {"title": "Approval-gated tool workflow", "level": "Advanced", "prerequisites": "Python functions, tools/APIs, and authorization concepts.", "hook": "Constrain tools with an allow-list and require approval before sensitive actions."},
    "mcp_kb": {"title": "Local knowledge-base MCP server", "level": "Advanced", "prerequisites": "Python, JSON-RPC, and client/server concepts.", "hook": "Expose local search and source reads as JSON-RPC-style tools."},
}
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

    counts = {level: sum(entry["level"] == level for entry in SYSTEMS.values()) for level in LEVEL_SUMMARIES}
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
        for name, info in SYSTEMS.items():
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
