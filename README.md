# Practical AI Systems

<p align="center">
  <strong>Small AI systems you can run, inspect, and evaluate.</strong><br />
  Practical builds for retrieval, extraction, agents, and reliability—with the failure cases included.
</p>

<p align="center">
  <a href="https://github.com/shivamnegi92/practical-ai-systems/actions/workflows/catalog.yml"><img src="https://github.com/shivamnegi92/practical-ai-systems/actions/workflows/catalog.yml/badge.svg" alt="Build and validation" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/content-CC0%201.0-lightgrey.svg" alt="CC0 1.0" /></a>
  <a href="systems/"><img src="https://img.shields.io/badge/runnable%20systems-10-2f6fdb.svg" alt="10 runnable systems" /></a>
</p>

**Build, run, and evaluate practical AI systems.** Start with a working baseline, see what breaks, then decide what deserves a model, more data, or more complexity.

## Run one now

```bash
git clone https://github.com/shivamnegi92/practical-ai-systems.git
cd practical-ai-systems
python3 -m systems.doc_qa.app "How much does Pro cost?"
```

No API key, package install, or model download. It searches the bundled sample docs and prints the source chunk. [See the system and its small eval →](systems/doc_qa/README.md)

## Featured builds

<table>
  <tr>
    <td width="33%" align="center">
      <a href="systems/doc_qa/README.md"><img src="docs/gallery/doc-qa.svg" alt="Document Q&A retrieves supporting passages, answers from evidence, and cites its source." width="100%"></a>
      <strong><a href="systems/doc_qa/README.md">Document Q&A</a></strong><br>
      <sub>Grounded answers, citations, and abstention.</sub>
    </td>
    <td width="33%" align="center">
      <a href="systems/voice_eval/README.md"><img src="docs/gallery/voice-eval.svg" alt="Voice-agent scorecard showing separate task success and forbidden-action rate." width="100%"></a>
      <strong><a href="systems/voice_eval/README.md">Voice Agent Eval</a></strong><br>
      <sub>Task success is not the same as safety.</sub>
    </td>
    <td width="33%" align="center">
      <a href="systems/bounded_agent/README.md"><img src="docs/gallery/tool-gate.svg" alt="A tool call passes an allow-list and pauses for human approval before a side effect." width="100%"></a>
      <strong><a href="systems/bounded_agent/README.md">Bounded Tool Workflow</a></strong><br>
      <sub>Allow-list, approval gate, then action.</sub>
    </td>
  </tr>
</table>

### Browse by category

<!-- SYSTEMS:START -->

> Ten small systems. Each one has runnable code, an offline test, a synthetic eval, and a README that tells you what the result does—and does not—mean.

**Pick a lane:** [Search & docs](#search-and-document-ai) · [Evaluation](#evaluation-and-reliability) · [Agents](#agents-and-integrations) · [Operations](#operations-and-developer-tools)

### Search and document AI

#### [Document Q&A with citations](systems/doc_qa/README.md)

Ask a question, retrieve the source paragraph, answer from its text, and abstain when the docs cannot support an answer.

**Fixture check:** answer contains expected fact **0.88** on 22 synthetic cases. Handwritten synthetic questions over bundled docs; this does not test broad-domain answer quality. [Details and cases](systems/doc_qa/eval/results.json).

#### [Invoice field extraction](systems/invoice_extract/README.md)

Turn invoice text into a typed schema, then reject dates and totals that fail basic validation.

**Fixture check:** exact field match **1.00** on 4 synthetic cases. Four plain-text fixtures; no OCR, locale variation, or real invoice layouts. [Details and cases](systems/invoice_extract/eval/results.json).

#### [Post-OCR document extraction](systems/multimodal_ocr/README.md)

Take OCR text plus bounding boxes, restore reading order, and extract invoice fields—without hiding the OCR boundary.

**Fixture check:** exact field match **1.00** on 3 synthetic cases. Three synthetic OCR-line fixtures; image recognition/OCR is not run or measured. [Details and cases](systems/multimodal_ocr/eval/results.json).

### Evaluation and reliability

#### [Entity spans and error analysis](systems/entity_extraction/README.md)

Extract person, date, and money spans and score exact offsets, so false positives are visible instead of polished away.

**Fixture check:** macro F1 across cases **0.63** on 4 synthetic cases. Four synthetic sentences and simple patterns; not a general NER benchmark. [Details and cases](systems/entity_extraction/eval/results.json).

#### [Voice-agent transcript evaluator](systems/voice_eval/README.md)

Score whether a call completed its task, triggered forbidden actions, and met response-latency expectations.

**Fixture check:** forbidden-action rate **0.33** on 3 synthetic cases. Three synthetic transcripts; latency is fixture metadata, not measured runtime. One seeded policy violation is detected. [Details and cases](systems/voice_eval/eval/results.json).

#### [Judge agreement audit](systems/judge_audit/README.md)

Compare a claim-checking judge with two human raters—and inspect when the humans themselves disagree.

**Fixture check:** heuristic/rater agreement **0.50** on 6 synthetic cases. Six synthetic labels and a lexical heuristic, not an LLM judge quality test. [Details and cases](systems/judge_audit/eval/results.json).

### Agents and integrations

#### [Approval-gated tool workflow](systems/bounded_agent/README.md)

Keep tools allow-listed, make plans immutable, and require explicit human approval before sensitive actions.

**Fixture check:** policy fixtures passed **1.00** on 3 synthetic cases. Three deterministic policy cases; no model planning or real external tools. [Details and cases](systems/bounded_agent/eval/results.json).

#### [Local knowledge-base MCP server](systems/mcp_kb/README.md)

Expose local document search and source-chunk reads as small tools over newline-delimited JSON-RPC.

**Fixture check:** expected chunk in top 3 **1.00** on 4 synthetic cases. Four synthetic queries; only an illustrative MCP-shaped subset, not client conformance-tested. [Details and cases](systems/mcp_kb/eval/results.json).

### Operations and developer tools

#### [Exact-response cache](systems/semantic_cache/README.md)

Avoid repeat work with normalized exact keys, model/version isolation, TTL expiry, and bounded LRU eviction.

**Fixture check:** exact replay rate **1.00** on 4 synthetic cases. Four exact-match fixtures; paraphrases intentionally miss. No production cost savings measured. [Details and cases](systems/semantic_cache/eval/results.json).

#### [Repository hygiene checks](systems/repo_guard/README.md)

A tiny, readable scanner catches a few obvious risky patterns and demonstrates why test fixtures matter.

**Fixture check:** precision on toy fixtures **1.00** on 4 synthetic cases. Four deliberately simple fixtures; not a security scanner or a substitute for maintained tooling. [Details and cases](systems/repo_guard/eval/results.json).
<!-- SYSTEMS:END -->

## Choose a learning path

<!-- PATHS:START -->

Browse curated workflows generated from the same catalog records—no project is duplicated across path docs.

- [Build a document-search baseline](catalog/paths.md#build-a-document-search-baseline)
- [Evaluate an AI feature before scaling it](catalog/paths.md#evaluate-an-ai-feature-before-scaling-it)
- [Operate a bounded tool-using agent](catalog/paths.md#operate-a-bounded-tool-using-agent)
<!-- PATHS:END -->

## Toolbox: curated projects

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

The catalog is a practical starting point, not a certification. A listing does not mean the project is endorsed, production-ready, secure, or independently benchmarked. Evidence labels show what this repo actually reviewed; check the linked source, license, terms, and operational fit before adopting anything.

- Only list public projects with a clear practical purpose, a canonical source, a candid limitation, direct license-file evidence, and a screened origin record with basis.
- Every project gets a provenance and governance review based on reliable public evidence. **Unclear means hold.**
- Do not copy third-party tutorials, code, data, screenshots, or README text. Link to canonical sources; respect their license

Browse curated workflows generated from the same catalog records—no project is duplicated across path docs.

- [Build a document-search baseline](catalog/paths.md#build-a-document-search-baseline)
- [Evaluate an AI feature before scaling it](catalog/paths.md#evaluate-an-ai-feature-before-scaling-it)
- [Operate a bounded tool-using agent](catalog/paths.md#operate-a-bounded-tool-using-agent)
e instructions.

## Refresh and validate

```bash
python3 scripts/build_


| Need | Browse |
|---|---|
| Build workflows that use tools, state, and human decisions. | [Agents and orchestration](catalog/agents.md) |
| Connect applications to search, documents, and indexed knowledge. | [Retrieval and knowledge systems](catalog/retrieval.md) |
| Turn text and documents into structured, usable data. | [Information extraction and document AI](catalog/extraction.md) |
| Build applications that handle images, audio, video, and interactive media. | [Multimodal application tools](catalog/multimodal.md) |
| Measure quality and inspect system behavior before and after release. | [Evaluation and observability](catalog/evaluation.md) |
| Package, serve, scale, and operate AI workloads. | [Deployment and operations](catalog/operations.md) |

**20 curated projects** across 6 system areas. Each record links to its canonical project and shows the review status.
