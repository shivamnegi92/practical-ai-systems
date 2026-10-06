---
name: practical-ai-systems-trend-curator
description: Use when refreshing, expanding, or auditing the Practical AI Systems GitHub catalog; discovering currently trending AI-agent, RAG, extraction, multimodal, evaluation, or deployment repositories; or updating its README based on new open-source projects.
user-invocable: true
argument-hint: "weekly | monthly | audit (optional)"
---

# Practical AI Systems Trend Curator

> **Project:** `/Users/s0n0611/Documents/GitHub/practical-ai-systems`
> **Inspiration:** Shubham Saboo's `awesome-llm-apps` and Nir Diamant's `agents-towards-production`, `GenAI_Agents`, and `RAG_Techniques`. Reuse high-level lessons—use-case categories, runnable examples, lifecycle breadth, explicit quality bars, and validation—not their text, code, assets, or entire lists.

## When to use

Use this skill to find timely projects and refresh or audit the Practical AI Systems catalog. Invoke from Claude Code in the repo with `/practical-ai-systems-trend-curator weekly`, `monthly`, or `audit`; no argument means `weekly`.

- **weekly:** inspect current trending/discovery sources, propose additions, update locally with eligible items, and write a dated report.
- **monthly:** broader discovery plus stale-entry, license, activity, and category review.
- **audit:** check current entries for URL, archive, license, origin-policy, and freshness changes without discovering additions.

Do not use for competitor pricing/assortment scraping or policy changes.

## Hard guardrails

- Discovery is not acceptance. Trending status, stars, or forks are signals—not quality rankings.
- **Provenance policy:** apply the maintainer's provenance policy (see the maintainer's private agent instructions). Assess the project/vendor/model itself from reliable public evidence; never infer origin from a contributor's name or nationality. If unclear, hold it—no guessing or substitution.
- **License:** verify current upstream license. Missing, custom, conflicting, or unclear terms mean `HOLD`; do not claim compatibility or copy upstream material.
- **Evidence:** record source URLs, retrieval timestamp and time zone, trend window/basis, and exact observed metrics if used. Do not invent rankings, trend counts, commit activity, or testing.
- **Local edits:** the user's request to run a refresh authorizes safe local catalog updates, but only after the hard checks pass. Keep uncertain entries out of active generated pages and explain them in `catalog/review-queue.json` plus the dated report. `report-only` or `dry-run` means no catalog edits.
- **No publishing:** never commit, push, create a GitHub repo, publish, or open a PR unless separately asked.
- **Preserve work:** check `git status --short` before edits. Never revert, overwrite, or include unrelated user changes. Canonical records live in `catalog/projects.json`; generated views are `catalog/*.md` and the README's `CATALOG` block. Do not edit generated files by hand.
- Do not mirror external catalogs wholesale or represent upstream work as Shivam's original work. Link canonical sources and attribute accurately.

## Discovery sources and research method

Use `web-retriever` for current GitHub Trending pages, repository discovery, and inspection of public repository pages. Do not use model memory as a substitute for current trending research. If browser/web retrieval fails, use reachable GitHub public API/search only if available; state the limitation and never claim a trending rank unless observed directly.

Inspect the configured sources in `catalog/trend-sources.json`, including:

- Shubham Saboo's `awesome-llm-apps` for application-oriented categories and discoverable examples.
- Nir Diamant's `agents-towards-production` for production lifecycle coverage and explicit tutorial quality bars.
- Nir Diamant's `GenAI_Agents` and `RAG_Techniques` for tutorial/scripts/evaluation/tests separation.

Use those repositories as discovery and structure references, not endorsements. Don't import their lists or content without candidate-by-candidate review.

For each candidate capture: canonical URL and owner/repo; category and use case; discovery source/window/date and observed rank or metrics (only if directly shown); current description; archived status; recent meaningful activity/release; license evidence; CI/tests/examples/dependency/contribution signals; origin evidence and confidence; duplicate check; one material tradeoff; rationale and decision.

Cover all six catalog categories where relevant: agents, retrieval, extraction, multimodal, evaluation, and operations. Keep the run manageable: normally 3–8 approved additions, not a firehose.

## Candidate decisions

**Reject** candidates that are dead links, unrelated, duplicates, policy conflicts, or unmaintained without clear historical utility. **Hold** candidates with unclear origin/license/status, inaccessible evidence, or insufficient trend evidence. High popularity never overrides a hard stop.

For viable items prioritize practical fit, active maintenance, clear documentation, examples, tests/CI, license clarity, and category diversity. The recommendation to add an entry should be reasoned, never based on stars alone.

## Workflow

1. **Baseline:** confirm repo path, inspect `git status --short`, read the current README, `catalog/projects.json`, category views, recipes, `catalog/review-queue.json`, and `catalog/trend-sources.json`. Do not use legacy update tooling as the active source of truth. Note pre-existing edits.
2. **Discover:** search the current requested period and the configured source repositories; verify candidates at canonical upstream sources.
3. **Check:** verify duplicates, archive/activity status, license, origin policy, and factual wording. Record uncertainty rather than smoothing it over.
4. **Report:** create `updates/YYYY-MM-DD.md` containing search window/timezone, sources checked, candidates added/held/rejected with evidence and reasons, stale-entry findings, proposed descriptions/tradeoffs, and access limitations.
5. **Apply locally:** unless `report-only`/`dry-run` was requested, add only fully eligible projects to `catalog/projects.json`. Place uncertain candidates in `catalog/review-queue.json` with reason and evidence; do not show them as active.
6. **Regenerate:** run `python3 scripts/build_catalog.py --write` to render README navigation and six category pages from canonical records.
7. **Validate:** run `python3 -m unittest discover -s tests -v`, `python3 scripts/build_catalog.py`, `git diff --check`; inspect exact diffs and report decisions and limitations. Never represent network failure as proof a link is dead.

### README and data structure

`catalog/projects.json` is the canonical active catalog; `scripts/build_catalog.py` renders six browsable `catalog/*.md` views and the marked README navigation block. Keep the opening promise, task journeys, original recipes, and inclusion policy human-edited. Candidate evidence belongs in `updates/YYYY-MM-DD.md`; unresolved candidates belong in `catalog/review-queue.json`. Do not use legacy `catalog/trend-additions.json` as an active source.

Each active project record must include a stable owner/repository ID, canonical URL, category, capabilities, delivery mode, factual summary, best-fit uses, concrete tradeoffs, SPDX and direct upstream `LICENSE` URL, origin evidence URL plus a short basis, current maintenance state/date, and evidence level. A screened origin without an evidence basis or a license based only on API metadata must fail validation. Do not add star counts by default; if popularity is relevant, record the source and date and treat it only as discovery context.

## Inspiration translated into project structure

- **Shubham:** browseable user/problem categories, fast entry points, runnable examples, and frequent incremental maintenance.
- **Nir:** cover the system lifecycle (build, data, retrieval, memory, security, evaluation, deployment); state a concrete quality bar; distinguish tutorial/notebook from runnable scripts, tests, evals, and assets.
- **This catalog:** make each item legible via category, practical use, limitation, source, license/origin evidence, and verification date. A curated index is not itself an endorsement or benchmark.

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

- Search window, retrieval time/timezone, and sources checked.
- Candidate counts and decisions: added, held, rejected—with reasons.
- Files changed and precise local update summary.
- Validation outcomes, including network/link limitations.
- Pre-existing unrelated changes preserved.
- Explicitly state that nothing was committed or pushed unless separately requested.
