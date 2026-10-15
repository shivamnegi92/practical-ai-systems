# Practical AI Systems

<p align="center">
  <strong>Learn to build practical AI systems, one runnable project at a time.</strong><br />
  Start with a first win. Move up when you’re ready. Every project includes code, tests, an evaluation, and honest limitations.
</p>

<p align="center">
  <a href="https://github.com/shivamnegi92/practical-ai-systems/actions/workflows/catalog.yml"><img src="https://github.com/shivamnegi92/practical-ai-systems/actions/workflows/catalog.yml/badge.svg" alt="Build and validation" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/content-CC0%201.0-lightgrey.svg" alt="CC0 1.0" /></a>
  <a href="systems/"><img src="https://img.shields.io/badge/runnable%20systems-30-2f6fdb.svg" alt="30 runnable systems" /></a>
</p>

## Pick your starting point

| Your experience | Start here | You’ll learn |
|---|---|---|
| **New to AI projects** | [Document Q&A](systems/doc_qa/README.md) | Find evidence in sample documents, answer with a citation, and abstain when the answer isn’t there. |
| **Some Python experience** | [Invoice extraction](systems/invoice_extract/README.md) | Extract structured fields and validate dates and totals. |
| **Building AI features professionally** | [Voice-agent evaluation](systems/voice_eval/README.md) | Measure task completion, unsafe actions, and latency separately. |

## Run your first project

You need Python 3.10+ and a terminal. No extra packages, model download, or API key required.

```bash
git clone https://github.com/shivamnegi92/practical-ai-systems.git
cd practical-ai-systems
python3 -m systems.doc_qa.app "How much does Pro cost?"
```

You should see an answer and the sample document chunk that supports it. Try an unsupported question too—the system should abstain. Then run the evaluation and tests:

```bash
python3 -m systems.doc_qa.evaluate
python3 -m unittest systems.doc_qa.test_doc_qa -v
```

Prefer a browser? Every project also ships a zero-dependency web app. Try them all in the [live gallery](https://shivamnegi92.github.io/practical-ai-systems/), or run one locally with `make serve SYSTEM=doc_qa` (needs Node 20+).

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

### Projects by experience level

<!-- SYSTEMS:START -->

Choose a level that feels right. You can skip ahead if you already know the basics.

- **[Beginner](#beginner)** — 10 first projects; no model setup.
- **[Intermediate](#intermediate)** — 10 projects; Python and basic metrics help.
- **[Advanced](#advanced)** — 10 projects; system boundaries and evaluation.

### Beginner

Start here if this is your first AI project. No model account or paid API key is needed.

#### [Document Q&A with citations](systems/doc_qa/README.md)

Find a source paragraph, answer from its evidence, cite it, or abstain.

**Before you start:** Terminal basics; Python is optional to run it.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/doc_qa/eval/results.json) · 22 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Invoice field extraction](systems/invoice_extract/README.md)

Extract invoice fields, then validate dates and arithmetic.

**Before you start:** Basic Python and key/value data.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/invoice_extract/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Repository hygiene checks](systems/repo_guard/README.md)

Run simple local checks and see why toy patterns miss real risks.

**Before you start:** Basic file and folder navigation.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/repo_guard/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Extractive text summarizer](systems/text_summarizer/README.md)

Pick the most representative sentences from a short document using word-frequency scoring.

**Before you start:** Terminal basics; Python is optional to run it.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/text_summarizer/eval/results.json) · 5 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Near-duplicate question detector](systems/dedupe_questions/README.md)

Flag probable duplicate support questions with token Jaccard similarity.

**Before you start:** Basic Python and string comparison.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/dedupe_questions/eval/results.json) · 5 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [PII pattern redactor](systems/pii_redactor/README.md)

Find and mask obvious email, phone, SSN, and credit-card-shaped strings in free text.

**Before you start:** Basic Python and regular expressions.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/pii_redactor/eval/results.json) · 5 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Lexicon-based sentiment classifier](systems/sentiment_lexicon/README.md)

Classify short text as positive, negative, or neutral using a small hand-built word list.

**Before you start:** Basic Python and word lists.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/sentiment_lexicon/eval/results.json) · 5 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Readability grade scorer](systems/readability_scorer/README.md)

Estimate a Flesch-Kincaid-style reading grade level and bucket it into simple/standard/complex.

**Before you start:** Basic Python; no linguistics background needed.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/readability_scorer/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [FAQ intent router](systems/faq_router/README.md)

Route a short support message to one of five fixed intents using keyword overlap.

**Before you start:** Basic Python and keyword matching.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/faq_router/eval/results.json) · 6 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [CSV/record schema validator](systems/csv_schema_validator/README.md)

Catch missing required fields and type mismatches in structured records before they reach an AI pipeline.

**Before you start:** Basic Python and JSON/dictionary data.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/csv_schema_validator/eval/results.json) · 5 small synthetic cases. Scores are learning fixtures, not production benchmarks.

### Intermediate

For people comfortable with basic Python who want to work with data and evaluation metrics.

#### [Post-OCR document extraction](systems/multimodal_ocr/README.md)

Normalize OCR line order from bounding boxes, then extract fields. OCR itself is not run.

**Before you start:** Basic Python and JSON/list/dictionary data.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/multimodal_ocr/eval/results.json) · 3 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Entity spans and error analysis](systems/entity_extraction/README.md)

Extract person/date/money spans and inspect exact-match precision, recall, and F1.

**Before you start:** Python functions, regular expressions, and basic metrics.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/entity_extraction/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Exact-response cache](systems/semantic_cache/README.md)

Explore normalized keys, TTL expiry, LRU eviction, and model/version isolation.

**Before you start:** Python classes, dictionaries, and basic cache concepts.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/semantic_cache/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Synonym query rewriter](systems/query_rewriter/README.md)

Expand a query with a small synonym list before BM25 retrieval, and measure the recall it recovers.

**Before you start:** Python functions and basic lexical retrieval.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/query_rewriter/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Prompt-injection pattern scanner](systems/prompt_injection_detector/README.md)

Scan untrusted text for common prompt-injection phrasing before it reaches a model.

**Before you start:** Regular expressions and basic LLM-safety concepts.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/prompt_injection_detector/eval/results.json) · 6 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Cost and latency guardrail tracker](systems/cost_latency_tracker/README.md)

Summarize a request log into p50/p95 latency and cost, then flag budget breaches.

**Before you start:** Basic statistics (percentiles) and Python.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/cost_latency_tracker/eval/results.json) · 3 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Post-OCR table reconstruction](systems/table_extractor/README.md)

Cluster OCR line bounding boxes into rows and columns to rebuild a simple table grid.

**Before you start:** Basic Python and coordinate geometry intuition.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/table_extractor/eval/results.json) · 2 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Image caption QC](systems/caption_qc/README.md)

Run rule-based checks on autogenerated image captions: placeholders, length, and required keywords.

**Before you start:** Basic Python and string checks.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/caption_qc/eval/results.json) · 5 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [RAG citation support checker](systems/citation_checker/README.md)

Verify that inline citations in a generated answer are lexically supported by the cited chunk.

**Before you start:** Basic Python and lexical overlap concepts.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/citation_checker/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Schema drift detector](systems/schema_drift_detector/README.md)

Diff a batch of records against a declared schema: new fields, missing fields, and type mismatches.

**Before you start:** Python dictionaries and basic data typing.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/schema_drift_detector/eval/results.json) · 2 small synthetic cases. Scores are learning fixtures, not production benchmarks.

### Advanced

For builders ready to reason about agent boundaries, protocols, and evaluation quality.

#### [Voice-agent transcript evaluator](systems/voice_eval/README.md)

Score call success, forbidden actions, and latency separately.

**Before you start:** Structured transcripts and evaluation rubrics.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/voice_eval/eval/results.json) · 3 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Judge agreement audit](systems/judge_audit/README.md)

Compare a heuristic with human ratings and inspect rater disagreement.

**Before you start:** Classification metrics and labeled data.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/judge_audit/eval/results.json) · 6 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Approval-gated tool workflow](systems/bounded_agent/README.md)

Constrain tools with an allow-list and require approval before sensitive actions.

**Before you start:** Python functions, tools/APIs, and authorization concepts.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/bounded_agent/eval/results.json) · 3 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Local knowledge-base MCP server](systems/mcp_kb/README.md)

Expose local search and source reads as JSON-RPC-style tools.

**Before you start:** Python, JSON-RPC, and client/server concepts.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/mcp_kb/eval/results.json) · 10 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Multi-agent triage handoff](systems/multi_agent_handoff/README.md)

Route a request through a triage step to the right specialist, escalating when confidence is low.

**Before you start:** Agent orchestration and escalation design.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/multi_agent_handoff/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Retrieval evaluation harness](systems/retrieval_eval_harness/README.md)

Score retrieval with recall@k, MRR, and nDCG@k, and compare two strategies side by side.

**Before you start:** IR evaluation metrics (recall, MRR, nDCG).

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/retrieval_eval_harness/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Canary rollout simulator](systems/canary_rollout_simulator/README.md)

Compare canary metrics against a baseline to decide promote or rollback.

**Before you start:** Deployment guardrails and basic statistics caveats.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/canary_rollout_simulator/eval/results.json) · 3 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Adversarial red-team harness](systems/redteam_harness/README.md)

Run adversarial requests against a bounded agent's policy and measure the breach rate.

**Before you start:** Agent authorization boundaries and adversarial thinking.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/redteam_harness/eval/results.json) · 5 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Trace anomaly detector](systems/trace_anomaly_detector/README.md)

Flag anomalous execution-trace durations with a z-score against a historical baseline.

**Before you start:** Basic statistics (mean, standard deviation, z-scores).

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/trace_anomaly_detector/eval/results.json) · 4 small synthetic cases. Scores are learning fixtures, not production benchmarks.

#### [Multi-hop reasoning router](systems/multi_hop_router/README.md)

Split a multi-part question into sub-questions and abstain unless every part is answered.

**Before you start:** Retrieval-augmented QA and question decomposition.

**Try this:** run the project README quickstart, then its test and evaluator.
[Evaluation results and cases](systems/multi_hop_router/eval/results.json) · 3 small synthetic cases. Scores are learning fixtures, not production benchmarks.
<!-- SYSTEMS:END -->

## Learning paths

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


## How to learn from a project

1. Choose a level using the prerequisites in its card.
2. Run the quickstart, then change one evaluation case and rerun it.
3. Inspect the result and read the stated limitations.

The evaluations use small synthetic fixtures. They are learning aids, not production benchmarks.

## For students and instructors

Use these examples as labs: run the baseline, change a case, and explain the outcome and failure modes. All included data is synthetic; results are learning fixtures, not evidence of real-world readiness.

## For professional teams

Treat examples as design patterns, not production services. Review data handling, authorization, dependencies, and evaluation gaps before adapting one to a real use case.

## Contribute

Contributions of every size are welcome—from a typo fix to a complete new system.
You do not need permission to propose an idea or open a pull request. **Nothing
merges without maintainer approval:** a pull request is a proposal, not a promise
of acceptance, and the maintainer reviews and approves every contributor PR.
This keeps the project open to ideas while the quality bar stays deliberate.

```bash
make check                                   # run everything CI runs
make new SYSTEM=my_system                    # scaffold a new system with Python, web app, tests, and npm lockfile
make test SYSTEM=doc_qa                      # test one system
make eval SYSTEM=doc_qa                      # regenerate its eval/results.json
make serve SYSTEM=doc_qa                     # open its web app at http://localhost:4173
```

- **5 minutes:** fix a README or [report a failing case](https://github.com/shivamnegi92/practical-ai-systems/issues/new?template=failing-case.yml).
- **30 minutes:** add eval cases that break a system, or improve a web app.
- **A few hours:** propose a new system with [`docs/ADDING_A_SYSTEM.md`](docs/ADDING_A_SYSTEM.md). Scope requests are welcome before implementation.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). Find [good first issues](https://github.com/shivamnegi92/practical-ai-systems/labels/good%20first%20issue) or [help-wanted tasks](https://github.com/shivamnegi92/practical-ai-systems/labels/help%20wanted). You may open a PR directly; opening or claiming an issue first is encouraged to avoid duplicate effort, not required for small changes. The maintainer makes the final merge decision.

## More resources

- [Learning paths](catalog/paths.md)
- [Curated project toolbox](catalog/README.md)
- [Original field guides](recipes/)
- [Evaluation playbook](benchmarks/README.md)
- [Changelog](CHANGELOG.md)

## License

Original material is released under [CC0 1.0](LICENSE). Linked projects retain their own licenses and terms.
