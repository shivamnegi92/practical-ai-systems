"""Validate structured catalog records and render browsable Markdown views."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "agents": ("Agents and orchestration", "Build workflows that use tools, state, and human decisions."),
    "retrieval": ("Retrieval and knowledge systems", "Connect applications to search, documents, and indexed knowledge."),
    "extraction": ("Information extraction and document AI", "Turn text and documents into structured, usable data."),
    "multimodal": ("Multimodal application tools", "Build applications that handle images, audio, video, and interactive media."),
    "evaluation": ("Evaluation and observability", "Measure quality and inspect system behavior before and after release."),
    "operations": ("Deployment and operations", "Package, serve, scale, and operate AI workloads."),
}
CAPABILITIES = {
    "tool-use", "agent-orchestration", "state-management", "retrieval", "vector-search",
    "hybrid-search", "document-parsing", "structured-extraction", "vision", "audio-video",
    "evaluation", "tracing", "deployment", "model-serving", "distributed-compute",
}
DELIVERY_MODES = {"framework", "library", "sdk", "database", "service", "tool", "platform", "engine"}
EVIDENCE_LEVELS = {"metadata-reviewed", "docs-reviewed", "smoke-tested", "independently-tested"}
REQUIRED_FIELDS = {
    "id", "name", "url", "category", "capabilities", "delivery_modes", "summary",
    "best_for", "tradeoffs", "license", "origin", "maintenance", "evidence_level",
}


def validate_records(records: object) -> list[str]:
    """Check record structure and hard inclusion-review gates."""
    if not isinstance(records, list):
        return ["catalog must be a list of project records"]
    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    for index, record in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = REQUIRED_FIELDS - record.keys()
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(sorted(missing))}")
            continue
        project_id = record["id"]
        if not isinstance(project_id, str) or not project_id.strip():
            errors.append(f"{prefix}.id must be non-empty")
        elif project_id.lower() in seen_ids:
            errors.append(f"{prefix} duplicate id: {project_id}")
        seen_ids.add(project_id.lower() if isinstance(project_id, str) else "")

        url = record["url"]
        parsed = urlparse(url) if isinstance(url, str) else None
        if not parsed or parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
            errors.append(f"{prefix}.url must be an https://github.com canonical URL")
        normalized_url = url.rstrip("/").lower() if isinstance(url, str) else ""
        if normalized_url in seen_urls:
            errors.append(f"{prefix} duplicate URL: {url}")
        seen_urls.add(normalized_url)

        if record.get("category") not in CATEGORIES:
            errors.append(f"{prefix}.category is not a supported category")
        for field in ("name", "summary"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        for field in ("best_for", "tradeoffs", "capabilities", "delivery_modes"):
            value = record.get(field)
            if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"{prefix}.{field} must be a non-empty list of strings")
        capabilities = record.get("capabilities") if isinstance(record.get("capabilities"), list) else []
        delivery_modes = record.get("delivery_modes") if isinstance(record.get("delivery_modes"), list) else []
        if all(isinstance(value, str) for value in capabilities):
            unknown_capabilities = set(capabilities) - CAPABILITIES
            if unknown_capabilities:
                errors.append(f"{prefix} unknown capabilities: {', '.join(sorted(unknown_capabilities))}")
        if all(isinstance(value, str) for value in delivery_modes):
            unknown_modes = set(delivery_modes) - DELIVERY_MODES
            if unknown_modes:
                errors.append(f"{prefix} unknown delivery modes: {', '.join(sorted(unknown_modes))}")

        license_info = record.get("license")
        evidence_url = license_info.get("evidence_url", "") if isinstance(license_info, dict) else ""
        if (
            not isinstance(license_info, dict)
            or license_info.get("status") != "verified"
            or not license_info.get("spdx")
            or not isinstance(evidence_url, str)
            or not evidence_url.endswith("/LICENSE")
        ):
            errors.append(f"{prefix}.license must cite an upstream LICENSE file and include verified SPDX evidence")
        origin = record.get("origin")
        if not isinstance(origin, dict) or origin.get("status") != "screened" or not origin.get("evidence_url") or not origin.get("basis"):
            errors.append(f"{prefix}.origin must be screened with evidence_url and basis for active catalog records")
        maintenance = record.get("maintenance")
        if not isinstance(maintenance, dict) or maintenance.get("status") != "active" or not maintenance.get("last_reviewed"):
            errors.append(f"{prefix}.maintenance must be active with last_reviewed date for active catalog records")
        if record.get("evidence_level") not in EVIDENCE_LEVELS:
            errors.append(f"{prefix}.evidence_level is not supported")
        trend = record.get("trend")
        if trend is not None:
            if not isinstance(trend, dict) or not trend.get("observed_at") or not trend.get("source") or not trend.get("basis"):
                errors.append(f"{prefix}.trend must record source, observed_at, and basis when present")
            if isinstance(trend, dict) and trend.get("rank") is not None and (not isinstance(trend["rank"], int) or trend["rank"] < 1):
                errors.append(f"{prefix}.trend.rank must be a positive integer")

    return errors


def _row(record: dict) -> str:
    name = record["name"].replace("|", "\\|")
    summary = record["summary"].replace("|", "\\|")
    best_for = "; ".join(record["best_for"]).replace("|", "\\|")
    tradeoffs = "; ".join(record["tradeoffs"]).replace("|", "\\|")
    modes = ", ".join(record["delivery_modes"])
    evidence = record["evidence_level"]
    return (
        f"| [{name}]({record['url']}) | {summary} | {best_for} | {tradeoffs} | "
        f"{modes} | {record['license']['spdx']} | {evidence} |"
    )


def render_category(category: str, records: list[dict]) -> str:
    """Render one category view from reviewed records."""
    if category not in CATEGORIES:
        raise ValueError(f"unknown category: {category}")
    title, description = CATEGORIES[category]
    items = sorted((item for item in records if item["category"] == category), key=lambda x: x["name"].casefold())
    lines = [f"# {title}", "", f"> {description}", "", "[← Back to Practical AI Systems](../README.md)", ""]
    if not items:
        lines.extend(["## Catalog", "", "No reviewed entries in this category yet. Suggest one using [the contribution guide](../CONTRIBUTING.md).", ""])
        return "\n".join(lines)
    lines.extend([
        "## Catalog", "",
        "Records are metadata-reviewed, not blanket endorsements.", "",
        "| Project | What it does | Best for | Tradeoffs to consider | Delivery | License | Evidence |",
        "|---|---|---|---|---|---|---|",
    ])
    lines.extend(_row(item) for item in items)
    lines.extend(["", "## Choosing well", "", "Start with the smallest component that solves the job. Validate it with your data, constraints, and failure cases before expanding the architecture.", ""])
    return "\n".join(lines)


def render_readme(readme: str, records: list[dict]) -> str:
    """Replace only the generated category index bounded by stable markers."""
    start_marker = "<!-- CATALOG:START -->"
    end_marker = "<!-- CATALOG:END -->"
    start = readme.find(start_marker)
    end = readme.find(end_marker)
    if start < 0 or end < 0 or end < start:
        raise ValueError("README must contain ordered CATALOG markers")
    lines = ["", "", "| Need | Browse |", "|---|---|"]
    for category, (title, desc) in CATEGORIES.items():
        lines.append(f"| {desc} | [{title}](catalog/{category}.md) |")
    lines.extend(["", f"**{len(records)} curated projects** across {len(CATEGORIES)} system areas. Each record links to its canonical project and shows the review status.", ""])
    begin = start + len(start_marker)
    return readme[:begin] + "\n" + "\n".join(lines) + readme[end:]


def check_generated(root: Path = ROOT) -> list[str]:
    """Return paths whose generated category or README views are stale."""
    records = json.loads((root / "catalog" / "projects.json").read_text(encoding="utf-8"))
    errors = validate_records(records)
    if errors:
        return errors
    readme = (root / "README.md").read_text(encoding="utf-8")
    if render_readme(readme, records) != readme:
        errors.append("README.md catalog index is stale; run scripts/build_catalog.py --write")
    for category in CATEGORIES:
        path = root / "catalog" / f"{category}.md"
        expected = render_category(category, records)
        if not path.exists() or path.read_text(encoding="utf-8") != expected:
            errors.append(f"{path.relative_to(root)} is stale; run scripts/build_catalog.py --write")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write generated README index and category pages")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    records_path = args.root / "catalog" / "projects.json"
    try:
        records = json.loads(records_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read {records_path}: {exc}", file=sys.stderr)
        return 2
    errors = validate_records(records)
    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    if args.write:
        readme_path = args.root / "README.md"
        readme_path.write_text(render_readme(readme_path.read_text(encoding="utf-8"), records), encoding="utf-8")
        for category in CATEGORIES:
            (args.root / "catalog" / f"{category}.md").write_text(render_category(category, records), encoding="utf-8")
        print(f"Rendered {len(records)} projects into README index and {len(CATEGORIES)} category pages.")
        return 0
    errors = check_generated(args.root)
    if errors:
        print("Generated catalog views are stale:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(records)} records and generated catalog views.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
