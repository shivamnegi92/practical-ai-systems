"""Validate structured catalog records and render browsable Markdown views."""

from __future__ import annotations

import argparse
import json
import re
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
REQUIRED_RECORD_FIELDS = {
    "id", "name", "url", "category", "capabilities", "delivery_modes", "summary",
    "best_for", "tradeoffs", "license", "origin", "maintenance", "evidence_level",
}
REQUIRED_PATH_FIELDS = {"id", "title", "summary", "audience", "steps"}
REQUIRED_STEP_FIELDS = {"title", "detail", "links", "project_ids"}


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
        missing = REQUIRED_RECORD_FIELDS - record.keys()
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


def render_readme(readme: str, records: list[dict], paths: list[dict]) -> str:
    """Replace only the generated category index bounded by stable markers."""
    start_marker = "<!-- CATALOG:START -->"
    end_marker = "<!-- CATALOG:END -->"
    path_start_marker = "<!-- PATHS:START -->"
    path_end_marker = "<!-- PATHS:END -->"
    markers = (start_marker, end_marker, path_start_marker, path_end_marker)
    if any(readme.count(marker) != 1 for marker in markers):
        raise ValueError("README must contain exactly one of each CATALOG and PATHS marker")
    start = readme.find(start_marker)
    end = readme.find(end_marker)
    path_start = readme.find(path_start_marker)
    path_end = readme.find(path_end_marker)
    if start < 0 or end < start:
        raise ValueError("README must contain ordered CATALOG markers")
    if path_start < 0 or path_end < path_start:
        raise ValueError("README must contain ordered PATHS markers")
    catalog_region = (start, end + len(end_marker))
    paths_region = (path_start, path_end + len(path_end_marker))
    if max(catalog_region[0], paths_region[0]) < min(catalog_region[1], paths_region[1]):
        raise ValueError("README CATALOG and PATHS generated regions must not overlap")
    lines = ["", "", "| Need | Browse |", "|---|---|"]
    for category, (title, desc) in CATEGORIES.items():
        lines.append(f"| {desc} | [{title}](catalog/{category}.md) |")
    lines.extend(["", f"**{len(records)} curated projects** across {len(CATEGORIES)} system areas. Each record links to its canonical project and shows the review status.", ""])
    begin = start + len(start_marker)
    readme = readme[:begin] + "\n" + "\n".join(lines) + readme[end:]

    path_begin = path_start + len(path_start_marker)
    path_links = ["", "Browse curated workflows generated from the same catalog records—no project is duplicated across path docs.", ""]
    for path in paths:
        anchor = re.sub(r"[^a-z0-9 -]", "", path["title"].lower()).replace(" ", "-")
        path_links.append(f"- [{path['title']}](catalog/paths.md#{anchor})")
    return readme[:path_begin] + "\n" + "\n".join(path_links) + "\n" + readme[path_end:]


def render_paths(paths: list[dict], records: list[dict]) -> str:
    """Render ordered decision paths from catalog IDs and local guides."""
    by_id = {record["id"]: record for record in records}
    lines = ["# Build paths", "", "> Short, evidence-aware routes through the catalog. These are starting points, not universal architectures.", ""]
    for path in paths:
        lines.extend([f"## {path['title']}", "", path["summary"], "", f"**For:** {path['audience']}", ""])
        for index, step in enumerate(path["steps"], start=1):
            lines.extend([f"### {index}. {step['title']}", "", step["detail"], ""])
            linked_projects = [f"[{by_id[project_id]['name']}]({by_id[project_id]['url']})" for project_id in step["project_ids"]]
            links = [
                f"[{link}](../{link})" if not link.startswith(("http://", "https://")) else f"[{link}]({link})"
                for link in step["links"]
            ]
            resources = linked_projects + links
            if resources:
                lines.extend(["**Explore:** " + " · ".join(resources), ""])
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def validate_paths(paths: object, records: list[dict], root: Path = ROOT) -> list[str]:
    """Check path metadata, project references, and local links."""
    errors: list[str] = []
    if not isinstance(paths, list):
        return ["paths must be a list"]
    record_ids = {record["id"] for record in records}
    seen_ids: set[str] = set()
    for index, path in enumerate(paths):
        prefix = f"paths[{index}]"
        if not isinstance(path, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("id", "title", "summary", "audience"):
            if not isinstance(path.get(field), str) or not path[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        path_id = path.get("id")
        if not isinstance(path_id, str) or not path_id.strip():
            errors.append(f"{prefix}.id must be a non-empty string")
            path_id = f"invalid-{index}"
        if path_id in seen_ids:
            errors.append(f"{prefix} duplicate path id: {path_id}")
        seen_ids.add(path_id)
        steps = path.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"{prefix}.steps must be a non-empty list")
            continue
        for step_index, step in enumerate(steps):
            step_prefix = f"{prefix}.steps[{step_index}]"
            if not isinstance(step, dict):
                errors.append(f"{step_prefix} must be an object")
                continue
            for field in ("title", "detail"):
                if not isinstance(step.get(field), str) or not step[field].strip():
                    errors.append(f"{step_prefix}.{field} must be a non-empty string")
            project_ids = step.get("project_ids")
            if not isinstance(project_ids, list) or any(not isinstance(item, str) for item in project_ids):
                errors.append(f"{step_prefix}.project_ids must be a list of strings")
            else:
                for project_id in project_ids:
                    if project_id not in record_ids:
                        errors.append(f"{step_prefix} unknown project ID: {project_id}")
            links = step.get("links")
            if not isinstance(links, list) or any(not isinstance(item, str) for item in links):
                errors.append(f"{step_prefix}.links must be a list of strings")
            else:
                for link in links:
                    if link.startswith(("https://", "http://")):
                        continue
                    target = (root / link).resolve()
                    if root.resolve() not in target.parents and target != root.resolve():
                        errors.append(f"{step_prefix} path escapes repository: {link}")
                    elif not target.exists():
                        errors.append(f"{step_prefix} missing local path: {link}")
    return errors


def check_generated(root: Path = ROOT) -> list[str]:
    """Return paths whose generated category or README views are stale."""
    records = json.loads((root / "catalog" / "projects.json").read_text(encoding="utf-8"))
    errors = validate_records(records)
    if errors:
        return errors
    paths = json.loads((root / "catalog" / "paths.json").read_text(encoding="utf-8"))
    path_errors = validate_paths(paths, records, root)
    errors.extend(path_errors)
    readme = (root / "README.md").read_text(encoding="utf-8")
    if render_readme(readme, records, paths) != readme:
        errors.append("README.md catalog/path index is stale; run scripts/build_catalog.py --write")
    paths_file = root / "catalog" / "paths.md"
    if not path_errors and (not paths_file.exists() or paths_file.read_text(encoding="utf-8") != render_paths(paths, records)):
        errors.append("catalog/paths.md is stale; run scripts/build_catalog.py --write")
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
    try:
        paths = json.loads((args.root / "catalog" / "paths.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read decision paths: {exc}", file=sys.stderr)
        return 2
    path_errors = validate_paths(paths, records, args.root)
    if path_errors:
        print("Decision path validation failed:", file=sys.stderr)
        print("\n".join(f"- {error}" for error in path_errors), file=sys.stderr)
        return 1
    if args.write:
        readme_path = args.root / "README.md"
        readme_path.write_text(render_readme(readme_path.read_text(encoding="utf-8"), records, paths), encoding="utf-8")
        for category in CATEGORIES:
            (args.root / "catalog" / f"{category}.md").write_text(render_category(category, records), encoding="utf-8")
        (args.root / "catalog" / "paths.md").write_text(render_paths(paths, records), encoding="utf-8")
        print(f"Rendered {len(records)} projects, {len(paths)} decision paths, and {len(CATEGORIES)} category pages.")
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
