"""Validate and render human-approved additions to the Practical AI Systems catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
START_MARKER = "<!-- TRENDING-CATALOG:START -->"
END_MARKER = "<!-- TRENDING-CATALOG:END -->"
CATEGORY_NAMES = {
    "agents": "Agents and orchestration",
    "retrieval": "Retrieval and knowledge systems",
    "extraction": "Information extraction and document AI",
    "multimodal": "Multimodal application tools",
    "evaluation": "Evaluation and observability",
    "operations": "Deployment and operations",
}
REQUIRED_FIELDS = {
    "name",
    "url",
    "category",
    "kind",
    "summary",
    "tradeoff",
    "license",
    "origin",
    "discovery",
    "archived",
    "stars",
}


def validate_catalog(catalog: dict) -> list[str]:
    """Return validation errors; only reviewed, attributable entries are publishable."""
    errors: list[str] = []
    entries = catalog.get("entries")
    if not isinstance(entries, list):
        return ["catalog.entries must be a list"]

    seen_urls: set[str] = set()
    for index, entry in enumerate(entries):
        prefix = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = REQUIRED_FIELDS - entry.keys()
        if missing:
            errors.append(f"{prefix} missing fields: {', '.join(sorted(missing))}")
            continue

        name = entry["name"]
        url = entry["url"]
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{prefix}.name must be a non-empty string")
        if not isinstance(url, str) or urlparse(url).netloc.lower() != "github.com":
            errors.append(f"{prefix}.url must be a canonical github.com repository URL")
        normalized_url = url.rstrip("/").lower() if isinstance(url, str) else ""
        if normalized_url in seen_urls:
            errors.append(f"{prefix} duplicate URL: {url}")
        seen_urls.add(normalized_url)
        if entry.get("category") not in CATEGORY_NAMES:
            errors.append(f"{prefix}.category is not a supported category")
        for field in ("kind", "summary", "tradeoff"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")

        if entry.get("archived") is not False:
            errors.append(f"{prefix}.archived must be false for a new catalog entry")
        stars = entry.get("stars")
        if (
            not isinstance(stars, dict)
            or not isinstance(stars.get("count"), int)
            or stars["count"] < 0
            or not stars.get("observed_at")
        ):
            errors.append(f"{prefix}.stars must contain a non-negative count and observed_at")

        license_info = entry.get("license")
        if not isinstance(license_info, dict) or license_info.get("status") != "verified":
            errors.append(f"{prefix}.license must have status 'verified'")
        elif not license_info.get("spdx") or not license_info.get("evidence"):
            errors.append(f"{prefix}.license must record spdx and evidence")

        origin_info = entry.get("origin")
        if not isinstance(origin_info, dict) or origin_info.get("status") != "screened":
            errors.append(f"{prefix}.origin must have status 'screened'")
        elif not origin_info.get("evidence"):
            errors.append(f"{prefix}.origin.evidence must be recorded")

        discovery = entry.get("discovery")
        if not isinstance(discovery, dict):
            errors.append(f"{prefix}.discovery must be an object")
        else:
            for field in ("source", "observed_at", "basis"):
                if not discovery.get(field):
                    errors.append(f"{prefix}.discovery.{field} must be recorded")

    return errors


def render_catalog(readme: str, catalog: dict) -> str:
    """Render accepted entries only into the explicitly managed README block."""
    start = readme.find(START_MARKER)
    end = readme.find(END_MARKER)
    if start < 0 or end < 0 or end < start:
        raise ValueError("README must contain ordered trending-catalog markers")
    current_entries = readme[:start] + readme[end + len(END_MARKER):]
    current_urls = {
        match.group(1).rstrip("/").lower()
        for match in re.finditer(r"\]\((https://github\.com/[^)]+)\)", current_entries, re.IGNORECASE)
    }
    proposed_urls = {entry["url"].rstrip("/").lower() for entry in catalog["entries"]}
    duplicates = current_urls & proposed_urls
    if duplicates:
        raise ValueError(f"repository URL already present outside generated region: {sorted(duplicates)[0]}")
    body_start = start + len(START_MARKER)
    entries = sorted(
        catalog["entries"],
        key=lambda item: (CATEGORY_NAMES[item["category"]].casefold(), item["name"].casefold()),
    )
    lines = ["", "", "## Recently reviewed discoveries", ""]
    lines.append(
        "> Candidates below were discovered from the cited trend/source observation and "
        "reviewed for this catalog. Popularity is a discovery signal, not a quality ranking."
    )
    lines.append("")
    for category, heading in CATEGORY_NAMES.items():
        items = [entry for entry in entries if entry["category"] == category]
        if not items:
            continue
        lines.extend([f"### {heading}", "", "| Project | Practical use | Tradeoff |", "|---|---|---|"])
        for entry in items:
            summary = entry["summary"].replace("|", "\\|").strip()
            tradeoff = entry["tradeoff"].replace("|", "\\|").strip()
            lines.append(f"| [{entry['name']}]({entry['url']}) | {summary} | {tradeoff} |")
        lines.append("")
    lines.extend(["<!-- Discovery records: catalog/trend-sources.json -->", ""])
    return readme[:body_start] + "\n" + "\n".join(lines) + readme[end:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=ROOT / "catalog" / "trend-additions.json")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    parser.add_argument("--apply", action="store_true", help="write rendered additions to README")
    args = parser.parse_args()

    try:
        catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read catalog JSON: {exc}", file=sys.stderr)
        return 2

    errors = validate_catalog(catalog)
    if errors:
        print("Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    try:
        readme = args.readme.read_text(encoding="utf-8")
        rendered = render_catalog(readme, catalog)
    except (OSError, ValueError) as exc:
        print(f"Cannot render README: {exc}", file=sys.stderr)
        return 2

    if not args.apply:
        print(f"Validated {len(catalog['entries'])} reviewed catalog additions; no files changed.")
        return 0

    args.readme.write_text(rendered, encoding="utf-8")
    print(f"Updated {args.readme} with {len(catalog['entries'])} reviewed additions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
