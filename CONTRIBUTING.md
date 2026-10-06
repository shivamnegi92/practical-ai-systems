# Contributing to Practical AI Systems

Thanks for helping builders choose and operate AI-system components responsibly. This is an evidence-backed catalog and field guide—not a popularity contest, product ranking, or home for copied tutorials.

## What belongs

A contribution should help someone make or evaluate a practical AI-system decision:

- add or correct a project record;
- improve an original recipe, failure-mode guide, or evaluation protocol;
- report stale links, changed license/status, or origin evidence;
- improve catalog tooling and tests.

Before proposing a new project, check `catalog/projects.json` and `catalog/review-queue.json` for duplicates or an existing hold.

## Project record requirements

Edit the canonical record in `catalog/projects.json`; generated category pages and the README index are not hand-edited. Each active entry requires:

Each active record needs: stable owner/repository ID; canonical URL; controlled category/capability/mode; factual summary, best-fit uses, tradeoffs; SPDX and direct `LICENSE` file URL; official origin evidence and a concise screening basis; maintenance review date; evidence level.

### Evidence levels

- `metadata-reviewed`: public metadata and evidence sources checked; no installation or independent testing implied.
- `docs-reviewed`: relevant upstream documentation read.
- `smoke-tested`: a narrow install/example test actually run and reproducible scope recorded.
- `independently-tested`: a documented test was run outside upstream claims with method/results available.

Never upgrade the evidence label based on intent or popularity.

## Origin, licenses, and attribution

- The active catalog excludes China-origin models, vendors, and frameworks. Evaluate the project/vendor/model itself with reliable public evidence; never infer origin from names or nationality. If unclear, put it in the review queue, not the active catalog.
- Verify a direct upstream license file, not API metadata alone. A recognized SPDX string does not grant permission for models, datasets, optional modules, or hosted services.
- Link to original work and write descriptions in your own words. Do not copy upstream prose, diagrams, code, datasets, or screenshots without compatible license and attribution.
- Explain hosted-vs-self-hosted boundaries, optional dependencies, and meaningful limitations where relevant.

## Path records

Use `catalog/paths.json` to assemble a user workflow from ordered steps. Link existing recipes, examples, and category pages; reference projects by stable ID in `project_ids`. Do not re-copy project descriptions into a path. The generator validates each ID and local file link, then renders `catalog/paths.md` and the README path block.


## Pull request workflow

1. Edit project records, decision paths, or original guides.
2. Run:

   ```bash
   python3 scripts/build_catalog.py --write
   python3 -m unittest discover -s tests -v
   python3 -m unittest discover -s tests -p 'test_paths.py' -v
   python3 -m unittest discover -s examples -p 'test_*.py' -v
   python3 scripts/build_catalog.py
   git diff --check
   ```

3. Inspect the generated README and category-page diffs; keep unrelated content untouched.
4. Include source links and a brief decision rationale in the PR.

Checklist:

- [ ] Canonical URL and current public status checked.
- [ ] No duplicate ID or URL.
- [ ] Category/capabilities/delivery modes accurately describe the project.
- [ ] Practical use and candid tradeoff included.
- [ ] License evidence and origin evidence linked.
- [ ] Origin policy passed; ambiguous cases held.
- [ ] Evidence label reflects what was actually checked/tested.
- [ ] No copied upstream material or unsupported ranking/security/production claim.
- [ ] Generated views and tests pass.

## Curation lifecycle

Active catalog records should be reviewed periodically. Move changed, archived, stale, or unresolved records to `catalog/review-queue.json` with the reason and date; do not silently delete history or keep a questionable entry active. Discovery reports belong in `updates/YYYY-MM-DD.md` and should distinguish observed facts from recommendations.
