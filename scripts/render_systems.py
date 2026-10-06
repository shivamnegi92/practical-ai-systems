"""Validate system metadata and render a category-first README gallery."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEMS = {
    "doc_qa": {
        "title": "Document Q&A with citations",
        "category": "Search and document AI",
        "hook": "Ask a question, retrieve the source paragraph, answer from its text, and abstain when the docs cannot support an answer.",
        "metric": "answer_contains_fact",
        "metric_label": "answer contains expected fact",
        "caveat": "Handwritten synthetic questions over bundled docs; this does not test broad-domain answer quality.",
    },
    "invoice_extract": {
        "title": "Invoice field extraction",
        "category": "Search and document AI",
        "hook": "Turn invoice text into a typed schema, then reject dates and totals that fail basic validation.",
        "metric": "field_exact_match",
        "metric_label": "exact field match",
        "caveat": "Four plain-text fixtures; no OCR, locale variation, or real invoice layouts.",
    },
    "multimodal_ocr": {
        "title": "Post-OCR document extraction",
        "category": "Search and document AI",
        "hook": "Take OCR text plus bounding boxes, restore reading order, and extract invoice fields—without hiding the OCR boundary.",
        "metric": "field_exact_match",
        "metric_label": "exact field match",
        "caveat": "Three synthetic OCR-line fixtures; image recognition/OCR is not run or measured.",
    },
    "entity_extraction": {
        "title": "Entity spans and error analysis",
        "category": "Evaluation and reliability",
        "hook": "Extract person, date, and money spans and score exact offsets, so false positives are visible instead of polished away.",
        "metric": "micro_like_average_f1",
        "metric_label": "macro F1 across cases",
        "caveat": "Four synthetic sentences and simple patterns; not a general NER benchmark.",
    },
    "voice_eval": {
        "title": "Voice-agent transcript evaluator",
        "category": "Evaluation and reliability",
        "hook": "Score whether a call completed its task, triggered forbidden actions, and met response-latency expectations.",
        "metric": "safety_violation_rate",
        "metric_label": "forbidden-action rate",
        "caveat": "Three synthetic transcripts; latency is fixture metadata, not measured runtime. One seeded policy violation is detected.",
    },
    "judge_audit": {
        "title": "Judge agreement audit",
        "category": "Evaluation and reliability",
        "hook": "Compare a claim-checking judge with two human raters—and inspect when the humans themselves disagree.",
        "metric": "judge_human_a_agreement",
        "metric_label": "heuristic/rater agreement",
        "caveat": "Six synthetic labels and a lexical heuristic, not an LLM judge quality test.",
    },
    "bounded_agent": {
        "title": "Approval-gated tool workflow",
        "category": "Agents and integrations",
        "hook": "Keep tools allow-listed, make plans immutable, and require explicit human approval before sensitive actions.",
        "metric": "policy_accuracy",
        "metric_label": "policy fixtures passed",
        "caveat": "Three deterministic policy cases; no model planning or real external tools.",
    },
    "mcp_kb": {
        "title": "Local knowledge-base MCP server",
        "category": "Agents and integrations",
        "hook": "Expose local document search and source-chunk reads as small tools over newline-delimited JSON-RPC.",
        "metric": "recall_at_3",
        "metric_label": "expected chunk in top 3",
        "caveat": "Four synthetic queries; only an illustrative MCP-shaped subset, not client conformance-tested.",
    },
    "semantic_cache": {
        "title": "Exact-response cache",
        "category": "Operations and developer tools",
        "hook": "Avoid repeat work with normalized exact keys, model/version isolation, TTL expiry, and bounded LRU eviction.",
        "metric": "exact_replay_rate",
        "metric_label": "exact replay rate",
        "caveat": "Four exact-match fixtures; paraphrases intentionally miss. No production cost savings measured.",
    },
    "repo_guard": {
        "title": "Repository hygiene checks",
        "category": "Operations and developer tools",
        "hook": "A tiny, readable scanner catches a few obvious risky patterns and demonstrates why test fixtures matter.",
        "metric": "precision",
        "metric_label": "precision on toy fixtures",
        "caveat": "Four deliberately simple fixtures; not a security scanner or a substitute for maintained tooling.",
    },
}
START = "<!-- SYSTEMS:START -->"
END = "<!-- SYSTEMS:END -->"


def _load_packet(folder: Path, name: str, info: dict) -> tuple[int, float]:
    required = [folder / "README.md", folder / "evaluate.py", folder / "eval" / "results.json"]
    if not all(path.exists() for path in required):
        raise ValueError(f"{name}: missing README, evaluation entrypoint, or eval/results.json")
    packet = json.loads((folder / "eval" / "results.json").read_text())
    if packet.get("system") != name or not packet.get("method"):
        raise ValueError(f"{name}: malformed evaluation packet")
    count = packet.get("dataset", {}).get("cases")
    metric = packet.get("metrics", {}).get(info["metric"])
    if not isinstance(count, int) or count <= 0 or not isinstance(metric, (int, float)):
        raise ValueError(f"{name}: missing sample count or metric {info['metric']!r}")
    return count, metric


def _render_entry(name: str, info: dict, count: int, metric: float) -> list[str]:
    readme = f"systems/{name}/README.md"
    results = f"systems/{name}/eval/results.json"
    return [
        f"#### [{info['title']}]({readme})",
        "",
        info["hook"],
        "",
        f"**Fixture check:** {info['metric_label']} **{metric:.2f}** on {count} synthetic cases. "
        f"{info['caveat']} [Details and cases]({results}).",
        "",
    ]


def render_readme(readme: str, root: Path = ROOT) -> str:
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one systems index marker pair")
    start, end = readme.index(START), readme.index(END)
    if end < start:
        raise ValueError("systems index markers out of order")

    categories: dict[str, list[tuple[str, dict, int, float]]] = {}
    for name, info in SYSTEMS.items():
        count, metric = _load_packet(root / "systems" / name, name, info)
        categories.setdefault(info["category"], []).append((name, info, count, metric))

    lines = [
        "",
        "> Ten small systems. Each one has runnable code, an offline test, a synthetic eval, and a README that tells you what the result does—and does not—mean.",
        "",
        "**Pick a lane:** [Search & docs](#search-and-document-ai) · [Evaluation](#evaluation-and-reliability) · [Agents](#agents-and-integrations) · [Operations](#operations-and-developer-tools)",
        "",
    ]
    for category, entries in categories.items():
        lines.extend([f"### {category}", ""])
        for name, info, count, metric in entries:
            lines.extend(_render_entry(name, info, count, metric))
    begin, finish = start + len(START), end
    return readme[:begin] + "\n" + "\n".join(lines) + readme[finish:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    path = args.root / "README.md"
    current = path.read_text()
    try:
        expected = render_readme(current, args.root)
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"System gallery validation failed: {exc}", file=sys.stderr)
        return 1
    if args.write:
        path.write_text(expected)
        print(f"Rendered a category-first gallery for {len(SYSTEMS)} systems.")
    elif expected != current:
        print("README system gallery is stale; run python scripts/render_systems.py --write", file=sys.stderr)
        return 1
    else:
        print(f"Validated the gallery for {len(SYSTEMS)} systems.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
