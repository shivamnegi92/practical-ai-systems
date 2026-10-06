# Retrieval and knowledge systems

> Connect applications to search, documents, and indexed knowledge.

[← Back to Practical AI Systems](../README.md)

## Catalog

Records are metadata-reviewed, not blanket endorsements.

| Project | What it does | Best for | Tradeoffs to consider | Delivery | License | Evidence |
|---|---|---|---|---|---|---|
| [Haystack](https://github.com/deepset-ai/haystack) | Compose search, retrieval, generation, and agent components into pipelines. | explicit pipeline composition; retrieval applications with inspectable components | Flexible pipelines still require task-specific evaluation, observability, and careful component selection. | framework | Apache-2.0 | metadata-reviewed |
| [LlamaIndex](https://github.com/run-llama/llama_index) | Connect data sources and retrieval components to data-connected AI applications. | document ingestion and retrieval prototypes; comparing indexing and query workflows | The integration surface is large; begin with only the connectors and abstractions your use case requires. | framework | MIT | metadata-reviewed |
| [Qdrant](https://github.com/qdrant/qdrant) | Vector database and similarity-search engine for retrieval applications. | vector search with metadata filtering; self-hosted or managed vector retrieval | Search quality depends on data preparation, embeddings, filters, and evaluation—not the database alone. | database, service | Apache-2.0 | metadata-reviewed |
| [Vespa](https://github.com/vespa-engine/vespa) | Search and serving platform for text, vector, and structured retrieval workloads. | large-scale hybrid search; ranking and serving with structured data | It has more operational and architectural surface area than a small vector-store deployment. | platform | Apache-2.0 | metadata-reviewed |

## Choosing well

Start with the smallest component that solves the job. Validate it with your data, constraints, and failure cases before expanding the architecture.
