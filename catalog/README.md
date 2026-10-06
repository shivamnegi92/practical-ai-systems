# Catalog data model

`projects.json` is the single source of truth for active projects. Category pages and the README's browse index are rendered with `scripts/build_catalog.py`; do not hand-edit generated views.

## Dimensions

Each project is classified along three orthogonal dimensions:

- **System layer (`category`)** — where it contributes in an AI application lifecycle.
- **Capability (`capabilities`)** — what it can do.
- **Delivery mode (`delivery_modes`)** — how a team consumes or operates it.

This lets us generate task-oriented views without duplicating project facts.

## Review fields

- `license`: verified SPDX identifier plus direct upstream `LICENSE` file URL; API metadata alone is insufficient.
- `origin`: `screened` status, official evidence URL, and a concise basis explaining what the cited sources establish.
- `maintenance`: status and last review date.
- `evidence_level`: what the catalog actually reviewed or tested.

## Adding an entry

1. Add one canonical record to `projects.json` using controlled values listed in `../scripts/build_catalog.py`.
2. Use a direct upstream `LICENSE` link; a GitHub API SPDX result alone is not enough. A screened origin must cite primary evidence and explain the basis. If license, origin, or maintenance is unclear, put the candidate in `review-queue.json` instead of active records.
5. The validator requires both values but does not prove the claim. Review the cited source yourself; validation passing is a structure check, not an origin verdict.

Popularity is never used as a proxy for quality or inclusion.
