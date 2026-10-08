# Catalog and field-guide restructure

**Date:** 2026-10-05
**Purpose:** Replace a long link list with structured project records, original practical guides, and validation.

## What changed

- Canonical external-project records live in `catalog/projects.json`, with category, capabilities, delivery mode, practical fit, trade-offs, license/provenance evidence, maintenance state, and evidence level.
- `scripts/build_catalog.py` validates records and renders six category pages plus the marked README toolbox section.
- Added original decision guides for document search, structured extraction, and bounded tool-using workflows, along with evaluation guidance.
- Added a dependency-free lexical retrieval example with runnable tests and explicit limitations.
- Added `catalog/review-queue.json` for candidates whose evidence is incomplete; held candidates are not rendered as active entries.
- Added contribution guidance, agent instructions, a pull-request checklist, and offline CI validation.

## Evidence scope

The catalog contains 20 metadata-reviewed external projects. That label does not mean software was installed, benchmarked, security-audited, or independently tested. Validation checks record structure; maintainers still review cited evidence.

## Validation

Offline tests cover malformed metadata, evidence gates, duplicates, rendering, README marker handling, and separation of held candidates. Generated views are checked against canonical records.
