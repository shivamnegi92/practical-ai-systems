# 10× Practical AI Systems Plan

## Goal
Make the public repository a trusted, discoverable, runnable decision guide for building practical AI systems—not merely a large catalog. Improve usefulness and sustainable contribution, not vanity metrics.

## Scope / principles
- Keep the current identity: curated decision layer across six system areas.
- Learn from Awesome LLM Apps (use-case navigation and runnable examples), Nir Diamant repositories (tutorial standards and lifecycle coverage), roadmap.sh (path-based discovery), and Made With ML (docs + tests + lifecycle teaching).
- Add only evidence-backed material; no copying, no unsupported rankings, and no China-origin models/vendors/frameworks.
- Avoid creating an interactive web product until static generated paths prove insufficient.
- Each phase should ship independently and leave CI green. Commit/push only after review and tests.

## Phases

| Phase | Status | Deliverable | Acceptance check |
|---|---|---|---|
| 0. Baseline and research | complete | Repo state, quality gaps, reference patterns | Clean main at 1b3e212; current public repo observed; findings saved |
| 1. Decision paths | complete | Three generated guides from project IDs and recipes | Tests validate project IDs/local links; generated pages current |
| 2. Evidence packets | planned | Add reproducibility metadata to records; design smaller smoke-test subset and explicit failure/report status | CI distinguishes metadata review from actual execution; no credential-required checks by default |
| 3. Freshness workflow | planned | Scheduled/manual report of stale records, upstream activity/license/archived drift | Reports stale items without silently editing claims; network errors are non-fatal and visible |
| 4. Contribution/release loop | planned | Issue templates, contribution checklist alignment, first tagged content release, changelog/update cadence | New contributor can propose a change and validate locally from README |
| 5. Discoverability polish | planned | Evaluate docs site/static generated views and visuals after path usage; add only if measurable benefit | No frontend until taxonomy/data model stable and users need richer navigation |

## Phase 1 delivered (local)
- Declarative paths created: document search, evaluation, bounded tool-using agent.
- Renderer generates `catalog/paths.md` and the README path block; project IDs and local refs are validated.
- Tests cover valid, missing, and stale path references and output generation.
- **Full validation passes:** 25 site/path tests, 4 example tests, generated-page validation, JSON parsing, local Markdown links, and `git diff --check`.

## Current status
Phase 1 is ready to publish. Phases 2–5 remain prioritized follow-on work, not an assertion that the whole 10× plan is complete.


## Explicit non-goals for this slice
- No new external AI model dependencies or hosted API calls.
- No star/fork tracking in active records.
- No large tutorial monorepo or all-upstream project copier.
- No paid demo or external service credentials.
- No redesign of the six category taxonomy unless testing exposes a concrete block.

## Validation commands
- `python3 -m unittest discover -s tests -v`
- `python3 -m unittest discover -s examples -p 'test_*.py' -v`
- `python3 scripts/build_catalog.py --write`
- `python3 scripts/build_catalog.py`
- `git diff --check`
- Check all internal Markdown links and ensure unrelated status changes are absent.

## Errors / constraints
- `ensure-dashboard.sh` referenced by planning-with-files was not present in the installed skill directory; use repo-local planning documents as working memory.
- GitHub public access/auth verified in prior task. Recheck before push.
