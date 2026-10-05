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
- **Origin policy:** do not include China-origin models, vendors, or frameworks. Assess the project/vendor/model itself from reliable public evidence; never infer origin from a contributor's name or nationality. If unclear, hold it—no guessing or substitution.
- **License:** verify current upstream license. Missing, custom, conflicting, or unclear terms mean `HOLD`; do not claim compatibility or copy upstream material.
- **Evidence:** record source URLs, retrieval timestamp and time zone, trend window/basis, and exact observed metrics if used. Do not invent rankings, trend counts, commit activity, or testing.
- **Local edits:** the user's request to run a refresh authorizes safe local catalog updates, but only after the hard checks pass. Keep uncertain entries out of the README and explain them in the report. `report-only` or `dry-run` means no README edits.
- **No publishing:** never commit, push, create a GitHub repo, publish, or open a PR unless separately asked.
- **Preserve work:** check `git status --short` before edits. Never revert, overwrite, or include unrelated user changes. Modify only the managed README region and dated report.
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

1. **Baseline:** confirm repo path, inspect `git status --short`, read `README.md`, `CONTRIBUTING.md`, `catalog/trend-sources.json`, and current entries. Note pre-existing edits.
2. **Discover:** search the current requested period and the configured source repositories; verify candidates at canonical upstream sources.
3. **Check:** verify duplicates, archive/activity status, license, origin policy, and factual wording. Record uncertainty rather than smoothing it over.
4. **Report:** create `updates/YYYY-MM-DD.md` containing search window/timezone, sources checked, candidates added/held/rejected with evidence and reasons, stale-entry findings, proposed descriptions/tradeoffs, and access limitations.
5. **Apply locally:** unless `report-only`/`dry-run` was requested, apply only entries that pass every hard check. Use a modest batch. The request to refresh is enough approval for these safe, local, reversible catalog changes; do not stop just to ask permission again. If safe isolation is impossible, do not edit and explain why.
6. **Validate:** run the commands below, inspect exact diffs, check only intended paths changed, and report all holds/rejections. Never represent SSL/network failure as a dead link.

### README and data structure

The current README is the easy-to-browse landing page. Keep its top-level user journeys and stable category navigation. New recurring discoveries go **only** between `<!-- TRENDING-CATALOG:START -->` and `<!-- TRENDING-CATALOG:END -->`; never replace the README wholesale. Avoid a monorepo of copied examples: link to canonical repos, label what was actually tested, and keep deep tutorials/tools as separate upstream projects unless they are authored here.

Each proposed structured entry in `catalog/trend-additions.json` must include:

- `name`, canonical `url`, `category`, `kind`, factual `summary`, candid `tradeoff`;
- `archived: false` and `stars: {count, observed_at}` (a dated snapshot; not an inclusion score);
- `license: {spdx, status: "verified", evidence}`;
- `origin: {status: "screened", evidence}`;
- `discovery: {source, observed_at, basis}`.

Use `catalog/trend-sources.json` for durable source configuration. Keep it concise; candidate evidence belongs in that run's dated update report. The current README entry format may differ from these structured inputs; render only after checking existing display conventions and reviewing the diff.

## Inspiration translated into project structure

- **Shubham:** browseable user/problem categories, fast entry points, runnable examples, and frequent incremental maintenance.
- **Nir:** cover the system lifecycle (build, data, retrieval, memory, security, evaluation, deployment); state a concrete quality bar; distinguish tutorial/notebook from runnable scripts, tests, evals, and assets.
- **This catalog:** make each item legible via category, practical use, limitation, source, license/origin evidence, and verification date. A curated index is not itself an endorsement or benchmark.

## Validation commands

Run from the repository root:

```bash
python3 scripts/catalog_update.py
python3 -m unittest discover -s tests -v
python3 -m json.tool catalog/trend-sources.json >/dev/null
python3 -m json.tool catalog/trend-additions.json >/dev/null
git diff --check
git status --short
```

Before rendering reviewed additions, inspect the intended diff. `catalog_update.py` without `--apply` validates only; `--apply` modifies only the marked README region. Never claim external links were checked if local TLS/network prevented verification; current browser/API evidence may still support checks.

## Finish with

- Search window, retrieval time/timezone, and sources checked.
- Candidate counts and decisions: added, held, rejected—with reasons.
- Files changed and precise local update summary.
- Validation outcomes, including network/link limitations.
- Pre-existing unrelated changes preserved.
- Explicitly state that nothing was committed or pushed unless separately requested.
