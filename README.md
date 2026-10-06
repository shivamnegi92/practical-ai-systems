# Practical AI Systems

<p align="center">
  <strong>A field guide to building AI systems that are useful, measurable, and operable.</strong><br />
  Tools are only the ingredients. This catalog helps you choose them, compose them, and know when they fail.
</p>

<p align="center">
  <a href="https://github.com/shivamnegi92/practical-ai-systems/actions/workflows/catalog.yml"><img src="https://github.com/shivamnegi92/practical-ai-systems/actions/workflows/catalog.yml/badge.svg" alt="Catalog validation" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/catalog%20content-CC0%201.0-lightgrey.svg" alt="CC0 1.0" /></a>
  <a href="catalog/README.md"><img src="https://img.shields.io/badge/catalog-structured%20%2B%20curated-2f6fdb.svg" alt="Structured catalog" /></a>
</p>

**Practical AI Systems is a curated decision layer for the AI application ecosystem.** Find the right building blocks, understand tradeoffs, and use original recipes to move from a demo to a system you can evaluate and operate.

> Not a framework, leaderboard, or copied link dump. Each active catalog record has a practical use, a caveat, upstream license evidence, an origin-policy review, and an explicit evidence level. Inclusion is not an endorsement or production-readiness guarantee.

## Choose a path

<!-- PATHS:START -->

Browse curated workflows generated from the same catalog records—no project is duplicated across path docs.

- [Build a document-search baseline](catalog/paths.md#build-a-document-search-baseline)
- [Evaluate an AI feature before scaling it](catalog/paths.md#evaluate-an-ai-feature-before-scaling-it)
- [Operate a bounded tool-using agent](catalog/paths.md#operate-a-bounded-tool-using-agent)
<!-- PATHS:END -->

## How the pieces fit

```text
Data & documents → Parse / extract → Retrieve / reason → Application / tools
        ↑                   ↓                 ↓                 ↓
  provenance       quality checks       evaluations      human control
        └──────── traces, deployment, security, feedback ────────┘
```

A useful system is a measured path through these layers—not a pile of agents. Start with the smallest design that solves the job; add complexity only when an observed failure calls for it.

## Browse the catalog

<!-- CATALOG:START -->


| Need | Browse |
|---|---|
| Build workflows that use tools, state, and human decisions. | [Agents and orchestration](catalog/agents.md) |
| Connect applications to search, documents, and indexed knowledge. | [Retrieval and knowledge systems](catalog/retrieval.md) |
| Turn text and documents into structured, usable data. | [Information extraction and document AI](catalog/extraction.md) |
| Build applications that handle images, audio, video, and interactive media. | [Multimodal application tools](catalog/multimodal.md) |
| Measure quality and inspect system behavior before and after release. | [Evaluation and observability](catalog/evaluation.md) |
| Package, serve, scale, and operate AI workloads. | [Deployment and operations](catalog/operations.md) |

**20 curated projects** across 6 system areas. Each record links to its canonical project and shows the review status.
<!-- CATALOG:END -->

### Evidence levels

- `metadata-reviewed` — public repository metadata and linked policy evidence were reviewed; code was not installed or independently tested.
- `docs-reviewed` — upstream documentation was read for the described use case.
- `smoke-tested` — a narrow install or example check ran, with date and scope recorded.
- `independently-tested` — a reproducible test ran outside the upstream project's own claims, with method/results linked.

The current seed is deliberately conservative: most entries are `metadata-reviewed`, **not** “tested” or “production-ready.” Candidates needing more origin or license evidence stay in the [review queue](catalog/review-queue.json), not in the active catalog. Record validation checks structure, not truth: a maintainer still must inspect the cited license and origin sources.

## Original field guides

These guides are written for this catalog; they synthesize decision-making and failure modes rather than copy upstream tutorials.

- [Document search: establish a retrieval baseline](recipes/document-search/README.md)
- [Runnable lexical baseline](examples/lexical_retrieval_baseline/README.md) — no dependencies or external credentials.
- [Structured extraction: validate outputs against reality](recipes/structured-extraction/README.md)
- [Tool-using workflows: bound autonomy with explicit control](recipes/tool-using-workflow/README.md)
- [Evaluation playbook: measure the task, not the demo](benchmarks/README.md)

## Project structure

```text
README.md                 Promise, task paths, guides, and policy
catalog/projects.json     Canonical structured project records
catalog/paths.json       Declarative learning paths over existing resources
catalog/*.md             Generated category pages and path guide
catalog/review-queue.json Candidates held for evidence/review
recipes/                 Original decision guides and system patterns
benchmarks/              Evaluation methodology and report template
updates/                 Dated curation/change reports
.claude/skills/           Project-local discovery and maintenance workflow
scripts/build_catalog.py Validate records; regenerate browsable views
examples/                 Small, tested baselines for system-building exercises
tests/                    Offline tests for policy, data, paths, and generated pages
```

## Inclusion and trust policy

- Only list public projects with a clear practical purpose, a canonical source, a candid limitation, direct license-file evidence, and a screened origin record with basis.
- Do not include China-origin models, vendors, or frameworks. Assess a project/vendor's origin using reliable public evidence; never infer from names or nationality. **Unclear means hold.**
- Do not copy third-party tutorials, code, data, screenshots, or README text. Link to canonical sources; respect their licenses.
- Popularity is a discovery signal, not a score. No bare star rankings or unsupported “best” claims.
- Check upstream security advisories, data handling, version support, and service terms before adopting a tool. The catalog is not a security audit or legal review.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the editorial and review bar, and [AGENTS.md](AGENTS.md) for repository maintenance instructions.

## Refresh and validate

```bash
python3 scripts/build_catalog.py --write
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s tests -p 'test_paths.py' -v
python3 -m unittest discover -s examples -p 'test_*.py' -v
python3 scripts/build_catalog.py
```

For weekly discovery, use the project-local [trend curator skill](.claude/skills/practical-ai-systems-trend-curator/SKILL.md). A scan produces a dated evidence report; only eligible candidates enter `catalog/projects.json`.

## License and attribution

Original catalog prose and recipes are released under [CC0 1.0](LICENSE). Each upstream project keeps its own license, trademarks, and terms; this catalog's license does not extend to linked resources. See each canonical project before reuse.

**Important:** `LICENSE` covers this repository's original material only. It does not grant rights to upstream code, models, datasets, logos, or linked projects.
