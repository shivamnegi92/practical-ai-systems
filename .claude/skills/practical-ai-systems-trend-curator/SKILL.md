---
name: practical-ai-systems-trend-curator
description: Refresh or audit the secondary toolbox of external AI projects using current public evidence.
user-invocable: true
argument-hint: "weekly | monthly | audit (optional)"
---

# Practical AI Systems Catalog Curator

> **Product:** Practical AI Systems is an original collection of runnable AI systems, each paired with an evaluation, failure cases, and implementation trade-offs. This skill maintains only the secondary toolbox of external projects; that toolbox is not the product.

## When to use

Use this skill to find timely external projects and refresh or audit the structured toolbox. Invoke with `/practical-ai-systems-trend-curator weekly`, `monthly`, or `audit`; no argument means `weekly`.

- **weekly:** discover candidates, review evidence, update eligible catalog records, and write a dated report.
- **monthly:** broader discovery plus a review of stale links, license/status changes, maintenance, and category coverage.
- **audit:** inspect current records for changes without discovering additions.

Do not use this skill for competitor pricing/assortment scraping or policy changes.

## Hard guardrails

- Discovery signals, stars, forks, and trending status are not quality rankings.
- Apply the maintainer's repository provenance policy using reliable public evidence. Assess the project/vendor/model itself; never infer based on a contributor's name or nationality. If unclear, hold it—no guessing or substitution.
- Verify a current upstream license file. Missing, custom, conflicting, or unclear terms mean `HOLD`; do not claim compatibility or copy upstream material.
- Record evidence URLs, retrieval date/time/time zone, discovery window, and observed metrics only when directly verified. Never invent ranks, activity, or test results.
- A refresh request permits safe local catalog edits only after required checks pass. `report-only` or `dry-run` means no catalog edits.
- Never commit, push, publish, create a repository, or open a PR unless separately asked.
- Check `git status --short` first. Preserve pre-existing user edits and never publish unrelated changes.
- The catalog is separate from the original runnable systems. Link to external work accurately; do not present it as authored here.

## Candidate discovery and review

Use current public GitHub Trending, repository search, releases, or other relevant discovery channels as leads only. Verify each candidate at its canonical source. No external list is a template, quality authority, or source to import wholesale.

For each candidate record its canonical URL and repository ID; category and use case; discovery source/date/window; archived and activity state; license evidence; documentation, examples, tests, and maintenance signals; provenance evidence and confidence; duplicate check; material trade-off; and decision.

Cover relevant catalog areas: agents, retrieval, extraction, multimodal, evaluation, and operations. Normally add only a few fully reviewed entries per run. **Reject** irrelevant, duplicate, dead, policy-conflicting, or clearly unmaintained items without historical value. **Hold** items with uncertain license, provenance, activity, or evidence.

## Workflow

1. **Baseline:** confirm repository location and inspect `git status --short`; read `README.md`, `catalog/projects.json`, generated category views, recipes, `catalog/review-queue.json`, and `catalog/trend-sources.json`. Note pre-existing edits.
2. **Discover:** inspect current discovery channels and verify potential candidates at canonical sources.
3. **Review:** check duplicates, archival/activity status, license, provenance, factual wording, and a concrete trade-off.
4. **Report:** create `updates/YYYY-MM-DD.md` with the search window/time zone, sources checked, decisions, evidence, limitations, and any access failures.
5. **Update locally:** add only fully eligible records to `catalog/projects.json`; put uncertain candidates in `catalog/review-queue.json`. Do not show held items as active.
6. **Regenerate and validate:** run the commands below; inspect the exact diff. A network failure is not proof that a project or link is dead.

## Data and generated views

`catalog/projects.json` is the canonical source for the external-project toolbox. `scripts/build_catalog.py` generates six category pages and the marked README toolbox section. Do not hand-edit generated views. Keep original runnable systems under `systems/`; do not mix them with third-party catalog entries.

Each active record needs a stable repository ID, canonical URL, category, capabilities, delivery mode, factual summary, best-fit uses, concrete trade-offs, SPDX identifier and direct license-file URL, provenance evidence URL plus a written basis, maintenance state/date, and evidence level. Validation checks structure; humans still need to inspect the cited evidence.

## Product boundary

The repository's own product is **original, runnable AI systems with evaluations, failure cases, and explicit trade-offs**. The external-project toolbox is a supporting feature. Describe that product on its own merits; do not frame it as a copy, derivative, or response to another repository.

## Validation commands

Run from the repository root:

```bash
python3 scripts/build_catalog.py --write
python3 -m unittest discover -s tests -v
python3 scripts/build_catalog.py
python3 -m json.tool catalog/projects.json >/dev/null
python3 -m json.tool catalog/review-queue.json >/dev/null
git diff --check
git status --short
```

## Finish with

Report the search window/time zone and sources checked; added/held/rejected counts and reasons; files changed; validation and access limitations; and confirm that no commit or push occurred unless separately requested.
