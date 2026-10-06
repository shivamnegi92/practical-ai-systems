# Practical AI Systems restructure

**Date:** 2026-10-05
**Purpose:** Move from a long README list to a structured, evidence-labeled decision catalog with original practitioner guides.

## Inspiration applied

Reviewed public structures from Shubham Saboo's `awesome-llm-apps` and Nir Diamant's `agents-towards-production`, `GenAI_Agents`, and `RAG_Techniques`. Adopted high-level patterns only: task-oriented navigation, explicit category boundaries, standalone learning resources, lifecycle coverage, clear contribution standards, and automated validation. No upstream README text, code, assets, notebooks, or lists were copied.

## What changed

- Canonical project records now live in `catalog/projects.json`, with category, capabilities, delivery mode, practical fit, tradeoffs, license/origin evidence, maintenance state, and evidence level.
- Added `scripts/build_catalog.py` to validate records and render the README browse index plus six category pages.
- Added original decision guides for document search, structured extraction, and bounded tool-using workflows, plus an evaluation protocol template.
- Added an original, dependency-free lexical retrieval example with runnable tests; it demonstrates a baseline and explicitly says what it cannot prove.
- Added `catalog/review-queue.json` for candidates with unresolved origin/license evidence. Browser Use remains held pending stronger project-origin evidence and is excluded from active pages.
- Expanded contribution standards, agent guidance, a pull-request checklist, and GitHub Actions validation for offline metadata/render/test checks.
- Retained the first-prototype trend scan report as historical provenance. `catalog/projects.json` and `scripts/build_catalog.py` are now the sole active catalog source of truth; the obsolete renderer and tests were removed.

## Evidence scope and limitation

The active catalog contains **20 metadata-reviewed** entries. License files and official project/organization sources were reviewed for each entry. `metadata-reviewed` does **not** mean the software was installed, benchmarked, security-audited, or independently tested. Category descriptions include explicit tradeoffs; the repository does not rank projects or claim comparative performance.

The review queue is intentionally visible: an ambiguous candidate is not silently promoted. Revisit those entries when stronger primary evidence is available.

## Validation

- Structured-record validation checks schema, controlled taxonomy, duplicate IDs/URLs, direct license-file URLs, origin evidence plus basis, maintenance state, and optional trend provenance. The validator checks structure—not the truth of cited claims; cited sources remain a human-review responsibility.
- Generated-view checks verify the README index and all six category pages match canonical records.
- Offline tests cover malformed metadata, evidence gates, duplicate detection, rendering, marker preservation, and review-queue separation.
