# Catalog data model

- `projects.json`: canonical active project records.
- `paths.json`: declarative user workflows composed from record IDs and local guides.
- `paths.md`: generated guided routes for common jobs (do not edit by hand).
- `*.md`: generated category views; do not hand-edit generated pages.

## Dimensions

Each project is classified along three orthogonal dimensions:

- **System layer (`category`)** — where it contributes in an AI application lifecycle.
- **Capability (`capabilities`)** — what it can do.
- **Delivery mode (`delivery_modes`)** — how a team consumes or operates it.

## Review fields

- `license`: verified SPDX identifier plus direct upstream `LICENSE` file URL; API metadata alone is insufficient.
- `origin`: `screened` status, official evidence URL, and a concise basis explaining what the cited sources establish.
- `maintenance`: active status and last review date.
- `evidence_level`: what the catalog actually reviewed or tested.

## Adding or reviewing records

1. Add a canonical record to `projects.json` using controlled values from `../scripts/build_catalog.py`.
2. Verify the upstream license file and source-backed origin. If either is unclear, keep the candidate in `review-queue.json`, not active records.
3. Add or update workflows in `paths.json` by referencing known project IDs and existing local guides; avoid duplicated descriptions.
4. Regenerate and test:

   ```bash
   python3 scripts/build_catalog.py --write
   python3 -m unittest discover -s tests -v
   python3 scripts/build_catalog.py
   ```

The validator checks structure and references; it cannot establish whether cited claims are true. Review primary sources yourself. Popularity is never a proxy for quality or inclusion.
