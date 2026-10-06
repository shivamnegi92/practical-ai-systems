# Plan: make Practical AI Systems a top-tier AI repository

_Last updated: 2026-10-05. Evidence: live GitHub API snapshot in `findings.md`._

## 1. The honest diagnosis

Today the repo is a well-engineered **catalog of other people's projects**: 20 links, 3 recipes, 1 runnable example, 0 stars, and no description, topics, or homepage on GitHub.

Every top repo we studied wins on **original artifacts people can run or fork**, not on curation quality. Validation pipelines are great hygiene, but nobody stars a schema. The catalog stays—as a supporting layer, not the product.

## 2. Patterns behind the winners (from the data)

| # | Pattern | Evidence | What it means for us |
|---|---|---|---|
| 1 | **A countable promise in one line** | "100+ AI Agents…", "21 Lessons", "42+ runnable notebooks", "50+ tutorials" | Headline must name a number of runnable things, and keep it true |
| 2 | **Original runnable units, not links** | awesome-llm-apps: 100+ app folders; Nir: notebook + script + tests per technique | Each unit = self-contained folder that runs in about 3 commands |
| 3 | **One strict template per unit** | Nir's tutorial contract; Microsoft's numbered lesson folders | Same README sections, layout, and eval format for every system |
| 4 | **Visible progression** | `starter_` / `advanced_` prefixes; lessons `00-`…`21-`; roadmap.sh paths | Levels + numbered paths (we already have paths, extend them) |
| 5 | **Ride each wave fast** | awesome-llm-apps added `mcp_ai_agents`, `agent_skills`, `voice_ai_agents`, `generative_ui_agents` as the topics peaked | Wave folders; ship within 1–2 weeks of a trend, using vetted tools only |
| 6 | **Author distribution flywheel** | llm-course: 83k stars, 3 contributors, README-only, backed by X/HF/blog/book; Shubham and Nir both run newsletters | Every new system gets a LinkedIn/X post + short write-up; distribution is half the work |
| 7 | **Low friction to first success** | devcontainers, `.env.example`, Colab badges in Microsoft/Nir repos | Local-first with Llama/Gemma/Mistral/Phi via Ollama; no paid key required to try |
| 8 | **Discoverability metadata** | Nir: 18–19 topics each; most winners have homepage + social preview; `llms.txt`, `CITATION.cff` | Fix GitHub metadata on day 1; add `llms.txt`, `CITATION.cff` |
| 9 | **Contribution mechanics** | 27–157 contributors; issue forms, contributor guides; Microsoft auto-translations drive forks | Issue forms, good-first-issues, contributor credit, system-request queue |
| 10 | **Sustained cadence** | All top repos pushed within the last few weeks; agents-towards-production reached ~21.5k stars in ~16 months | Weekly shipping beats one big drop |

## 3. Positioning: the wedge

Cloning awesome-llm-apps at 140k stars is a losing game. The gap none of them fill well: **every example is evaluated.**

> **Practical AI Systems — 50 production-shaped AI systems you can run on a laptop. Each one ships with an eval suite, failure modes, and cost/latency numbers.**

Why this wedge:
- It matches Shivam's real strengths (voice-agent evaluation, entity/multimodal extraction, evaluation discipline).
- Defaults run on widely used open-weight models through a local provider, so anyone can try every system for free.
- It produces genuine, measurable open-source adoption (forks, citations, contributors).
- Hard to copy cheaply: anyone can wrap an LLM call; few ship reproducible evals.

## 4. The unit of content: a "system"

```text
systems/<area>/<level>-<slug>/
  README.md        problem -> architecture diagram -> run in 3 commands -> eval results -> failure modes -> cost/latency -> extend it
  app/             minimal code (CLI or small UI)
  eval/            small labeled dataset (synthetic or properly licensed) + eval script + results.json
  tests/           offline tests using a stub model (CI never needs keys)
  demo.gif         10-20 second visual
  requirements.txt / pyproject.toml
```

Levels: `starter`, `intermediate`, `advanced`. Areas reuse the existing six categories (agents, retrieval, extraction, multimodal, evaluation, operations) plus wave folders (`mcp`, `agent-skills`, `voice`).

Generated index: extend `scripts/build_catalog.py` so that each system's front-matter generates README tables and paths. One source of truth, the same DRY approach as the catalog today.

## 5. Phased plan

### Phase 0 — Packaging and foundation (week 1)
- [ ] GitHub description, ~15 topics, social preview image, homepage (set later when a docs site exists).
- [ ] README rewrite: countable promise, demo GIF, "Start here in 5 minutes", systems table by area/level.
- [ ] `systems/_template/` + system contract in `CONTRIBUTING.md`.
- [ ] Shared `common/llm.py`: one provider interface (Ollama local default, optional hosted APIs) + a stub provider for tests.
- [ ] CI: build index, run every system's offline tests, link check.
- [ ] `llms.txt`, `CITATION.cff`, `.env.example`, devcontainer.
- [ ] Move `catalog/` under a "Toolbox" section—supporting, not the headline.

### Phase 1 — Flagship content sprint (weeks 1–4): 10 systems before launch
Seed list (adjust to taste; favor Shivam's existing work so attention consolidates instead of scattering):
1. Document Q&A with retrieval eval (recall@k, answer faithfulness) — starter
2. Invoice/receipt structured extraction with field-level accuracy — starter
3. Entity extraction pipeline + error analysis (port Shivam's work) — intermediate
4. Voice agent evaluation harness (port `voice-agent-eval-corpus`) — advanced
5. Multimodal document extraction (port existing project) — intermediate
6. Bounded tool-using agent with guardrails + approval step — intermediate
7. MCP server for a local knowledge base — wave
8. LLM-as-judge done carefully: judge agreement vs. human labels — intermediate
9. Semantic cache + cost/latency dashboard — operations
10. Agent skill: repo-maintenance skill with an eval (dogfoods our trend curator) — wave

Acceptance per system: runs locally in 3 commands or fewer, eval results committed, offline tests green, GIF recorded, and no copied third-party tutorial content.

### Phase 2 — Launch (end of week 4, not before)
- [ ] Launch only with 10 or more working systems; an empty repo wastes the one first impression.
- [ ] Coordinated posts: LinkedIn (long-form), X thread, Show HN, r/LocalLLaMA, relevant Discords.
- [ ] Each post leads with one striking eval finding (e.g., "the judge disagreed with humans 31% of the time"), not with "I made a repo."
- [ ] Submit to awesome lists where genuinely relevant.

### Phase 3 — Cadence and waves (months 2–3): 30 systems
- [ ] Ship 2 systems/week; "New this week" section generated in the README.
- [ ] Wave watch: run the trend-curator skill weekly; when a topic peaks, ship a system within 1–2 weeks (only vetted, policy-compliant tools).
- [ ] One write-up per system (LinkedIn/blog), linking back to the folder.

### Phase 4 — Community engine (month 3+)
- [ ] Issue forms: system request, new system proposal, bug, stale entry.
- [ ] Label 10 good-first-issues at all times (e.g., add an eval case, port to another local model).
- [ ] Contributor credit in each system README + an all-contributors table.
- [ ] Review SLA: first response within 72 hours.

### Phase 5 — Scale and authority (months 4–6): 50+ systems
- [ ] Docs site (MkDocs or Astro) generated from the same metadata; only now, once content justifies it.
- [ ] Cross-system results page: comparable eval numbers across local models (reproducible, with exact versions, no "best" claims).
- [ ] Optional: notebook/Colab variants for the most popular systems, translations driven by demand.
- [ ] Talks/meetups and a short e-book or course built from the repo.

### Folded-in maintenance (from the earlier backlog)
- Evidence packets → now inherent: each system's `eval/results.json` is the evidence.
- Freshness workflow → monthly read-only audit of catalog links and system dependencies; reports, never silently edits.
- Release loop → monthly tagged release + CHANGELOG ("v0.3: 6 new systems").

## 6. Metrics (leading indicators first)

| Metric | 30 days | 90 days | 6 months |
|---|---|---|---|
| Runnable systems with evals | 10 | 30 | 50+ |
| Median time-to-first-run (fresh clone) | < 10 min | < 5 min | < 5 min |
| External PRs merged | 0–2 | 10 | 40 |
| Distinct contributors | 1–3 | 10 | 25+ |
| Posts/write-ups published | 4 | 20 | 40 |

Stars and forks are outcomes, not plans; track them monthly (GitHub traffic API: views, clones, referrers) and use referrers to double down on channels that work. Keep a monthly adoption snapshot.

## 7. What we will not do
- Buy stars, run star-for-star swaps, or post spammy self-promotion.
- Copy or lightly reskin other repos' tutorials.
- Ship 100 shallow API wrappers to inflate the headline number.
- Add models, vendors, or frameworks that fail the maintainer provenance review (unclear means hold).
- Launch before 10 solid systems exist.
- Build a docs site before the content exists to fill it.

## 8. Risks and constraints
- **Independence:** personal project. No employer-internal code, data, names, or branding, and nothing implying any employer's endorsement.
- **Time capacity:** 2 systems/week is ambitious beside a day job; quality over count—drop to 1/week before lowering the bar.
- **Cost:** local-first by default keeps it free for us and for users.
- **Data licensing:** eval datasets must be synthetic or clearly licensed; no PII.
- **Maintenance debt:** pin dependencies; monthly freshness audit; archive systems that rot rather than leaving them broken.

## 9. Immediate next actions
1. Set GitHub description + topics (5 minutes, highest ROI).
2. Build `systems/_template/`, `common/llm.py` with stub provider, and index generation (test-first).
3. Ship system #1 (document Q&A with retrieval eval) end-to-end as the reference implementation.
4. Rewrite README around the new promise once system #1 exists.
