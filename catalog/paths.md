# Build paths

> Short, evidence-aware routes through the catalog. These are starting points, not universal architectures.

## Build a document-search baseline

Parse documents, retrieve candidate evidence, then evaluate before adding answer generation.

**For:** Builders starting a document-grounded application.

### 1. Define representative questions

Include answerable, ambiguous, and unanswerable examples with source evidence.

**Explore:** [recipes/document-search/README.md](../recipes/document-search/README.md) · [benchmarks/README.md](../benchmarks/README.md)

### 2. Parse with source provenance

Keep document version, page/section, and access-control metadata attached.

**Explore:** [Docling](https://github.com/docling-project/docling) · [Apache Tika](https://github.com/apache/tika) · [catalog/extraction.md](../catalog/extraction.md)

### 3. Run a simple lexical baseline

Inspect which source passages a deterministic token-overlap baseline retrieves.

**Explore:** [examples/lexical_retrieval_baseline/README.md](../examples/lexical_retrieval_baseline/README.md)

### 4. Compare retrieval approaches on the same labels

Measure recall and failure slices before adding generation.

**Explore:** [LlamaIndex](https://github.com/run-llama/llama_index) · [Haystack](https://github.com/deepset-ai/haystack) · [Qdrant](https://github.com/qdrant/qdrant) · [catalog/retrieval.md](../catalog/retrieval.md) · [benchmarks/README.md](../benchmarks/README.md)

### 5. Add answers with citations last

Require support from retrieved evidence and allow abstention when it is missing.

**Explore:** [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) · [recipes/document-search/README.md](../recipes/document-search/README.md) · [catalog/evaluation.md](../catalog/evaluation.md)

---

## Evaluate an AI feature before scaling it

Translate a user task into a reproducible test set, compare against a baseline, and inspect failure costs.

**For:** Teams deciding whether an AI feature is reliable enough to expand.

### 1. Define success and failure cost

Specify the user-visible outcome and the costly mistakes, not just response fluency.

**Explore:** [benchmarks/README.md](../benchmarks/README.md)

### 2. Build a representative labeled set

Include normal, edge, ambiguous, and unanswerable cases; record data provenance.

**Explore:** [benchmarks/README.md](../benchmarks/README.md) · [recipes/structured-extraction/README.md](../recipes/structured-extraction/README.md)

### 3. Run a simple baseline

Compare the smallest design to the proposed system under the same conditions.

**Explore:** [examples/lexical_retrieval_baseline/README.md](../examples/lexical_retrieval_baseline/README.md)

### 4. Track quality and runtime signals

Inspect errors, slices, latency, cost, and traces; do not collapse everything into one score.

**Explore:** [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) · [catalog/evaluation.md](../catalog/evaluation.md) · [catalog/operations.md](../catalog/operations.md)

### 5. Publish a reproducible decision record

Capture versions, conditions, limitations, and what decision the result supports.

**Explore:** [benchmarks/README.md](../benchmarks/README.md)

---

## Operate a bounded tool-using agent

Begin with a deterministic workflow, permit only justified model decisions, and put authorization outside the model.

**For:** Builders adding tools or actions to an AI application.

### 1. Write the deterministic workflow first

Mark only decision points that genuinely depend on uncertain context.

**Explore:** [recipes/tool-using-workflow/README.md](../recipes/tool-using-workflow/README.md)

### 2. Define tool authority and side effects

Use least privilege, typed arguments, explicit approvals, retries, and idempotency.

**Explore:** [Semantic Kernel](https://github.com/microsoft/semantic-kernel) · [LangGraph](https://github.com/langchain-ai/langgraph) · [recipes/tool-using-workflow/README.md](../recipes/tool-using-workflow/README.md)

### 3. Exercise failure and refusal paths

Test malformed tool results, timeouts, replay, untrusted input, and unauthorized actions.

**Explore:** [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) · [catalog/evaluation.md](../catalog/evaluation.md) · [benchmarks/README.md](../benchmarks/README.md)

### 4. Deploy only the minimum runtime

Choose serving and orchestration infrastructure based on measured scale needs.

**Explore:** [BentoML](https://github.com/bentoml/BentoML) · [Docker Compose](https://github.com/docker/compose) · [Kubernetes](https://github.com/kubernetes/kubernetes) · [catalog/operations.md](../catalog/operations.md)

---
