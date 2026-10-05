# Practical AI Systems

> A practitioner-first catalog of useful AI systems: discover the tools, patterns, and runnable examples behind applications—from extraction and retrieval to agents, multimodal workflows, evaluation, and deployment.

**Not another model leaderboard or link dump.** This catalog helps builders choose a practical starting point, understand tradeoffs, and find maintained projects. Entries link to their canonical sources; inclusion is not an endorsement, security audit, or guarantee of production readiness.

## Start here

| I want to… | Start with… |
|---|---|
| Build an agent or tool-using workflow | [Agents and orchestration](#agents-and-orchestration) |
| Search my documents or build RAG | [Retrieval and knowledge systems](#retrieval-and-knowledge-systems) |
| Extract structured data from text or files | [Information extraction and document AI](#information-extraction-and-document-ai) |
| Build a vision/audio/video application | [Multimodal application tools](#multimodal-application-tools) |
| Evaluate, trace, and improve an AI application | [Evaluation and observability](#evaluation-and-observability) |
| Run models or applications reliably | [Deployment and operations](#deployment-and-operations) |

## How to read this catalog

- **Type** identifies the project kind: framework, library, service, or tool.
- **Use it for** describes the practical fit, not a benchmark claim.
- **Tradeoff** is a reminder to validate the project against your constraints.
- **Verified** records when the public repository status/link was last checked. It does not mean every feature was independently tested.
- A link means “consider this resource,” not “the maintainers endorse it.” Check the canonical project for current docs, license, security advisories, and support status before adopting it.

## Catalog

### Agents and orchestration

| Project | Type | Use it for | Tradeoff | Verified |
|---|---|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Framework | Stateful, graph-structured agent and workflow orchestration. | Explicit state and orchestration are powerful, but require deliberate design. | 2026-10-05 |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Framework | Building role-based agent teams and task workflows. | Multi-agent abstractions can increase latency and cost; check whether one agent is enough. | 2026-10-05 |
| [AutoGen](https://github.com/microsoft/autogen) | Framework | Creating agentic applications and conversations between agents and tools. | APIs evolve; pin versions and verify migration guidance. | 2026-10-05 |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | SDK | Adding AI orchestration, plugins, and memory to applications. | Broad abstractions need provider, portability, and version choices made explicit. | 2026-10-05 |

### Retrieval and knowledge systems

| Project | Type | Use it for | Tradeoff | Verified |
|---|---|---|---|---|
| [LlamaIndex](https://github.com/run-llama/llama_index) | Framework | Connecting data sources to retrieval and LLM application workflows. | Large integration surface; start with the smallest set of components you need. | 2026-10-05 |
| [Haystack](https://github.com/deepset-ai/haystack) | Framework | Composing retrieval, search, generation, and agent pipelines. | Flexible pipelines still need task-specific evaluation and monitoring. | 2026-10-05 |
| [Qdrant](https://github.com/qdrant/qdrant) | Vector database | Vector search and similarity retrieval for AI applications. | Retrieval quality also depends on chunking, embeddings, filters, and evaluation. | 2026-10-05 |
| [Vespa](https://github.com/vespa-engine/vespa) | Search platform | Large-scale hybrid search over text, vectors, and structured data. | Powerful platform with higher operational complexity than a simple vector store. | 2026-10-05 |

### Information extraction and document AI

| Project | Type | Use it for | Tradeoff | Verified |
|---|---|---|---|---|
| [Docling](https://github.com/docling-project/docling) | Document toolkit | Parsing documents and converting layout-aware content into AI-ready representations. | Validate against your actual document types, languages, and layouts. | 2026-10-05 |
| [Unstructured](https://github.com/Unstructured-IO/unstructured) | Document toolkit | Ingesting varied file formats into structured content for downstream applications. | Review the open-source/commercial feature boundary and deployment requirements. | 2026-10-05 |
| [Apache Tika](https://github.com/apache/tika) | Content analysis toolkit | Detecting file types and extracting text and metadata from many formats. | A parser foundation, not a complete layout-aware document-understanding pipeline. | 2026-10-05 |
| [MarkItDown](https://github.com/microsoft/markitdown) | Conversion tool | Converting files and office documents to Markdown for downstream workflows. | Conversion may lose layout or relationships that matter for precise extraction. | 2026-10-05 |
| [OCRmyPDF](https://github.com/ocrmypdf/OCRmyPDF) | PDF tool | Adding searchable OCR text layers to scanned PDFs. | Accuracy depends on source scans and language settings; check output before relying on it. | 2026-10-05 |

### Multimodal application tools

| Project | Type | Use it for | Tradeoff | Verified |
|---|---|---|---|---|
| [Gradio](https://github.com/gradio-app/gradio) | App framework | Building interactive demos and Python interfaces for machine-learning applications. | Production authentication, isolation, and scaling need additional design. | 2026-10-05 |
| [Streamlit](https://github.com/streamlit/streamlit) | App framework | Quickly building data and AI applications in Python. | Complex multi-user products may need a more conventional web architecture. | 2026-10-05 |
| [OpenCV](https://github.com/opencv/opencv) | Computer-vision library | Image and video processing primitives for application pipelines. | Low-level primitives require application-specific logic and testing. | 2026-10-05 |
| [FFmpeg](https://github.com/FFmpeg/FFmpeg) | Media toolkit | Processing, converting, decoding, and streaming audio/video. | Codec, deployment, and licensing choices need careful review. | 2026-10-05 |

### Evaluation and observability

| Project | Type | Use it for | Tradeoff | Verified |
|---|---|---|---|---|
| [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) | Telemetry collector | Receiving, processing, and exporting vendor-neutral telemetry. | AI-specific instrumentation and dashboards still need to be designed. | 2026-10-05 |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | Observability/evaluation | Tracing and analyzing LLM application behavior and evaluations. | Useful evaluation depends on representative data and meaningful graders. | 2026-10-05 |
| [Langfuse](https://github.com/langfuse/langfuse) | Observability/evaluation | Tracing, evaluating, and improving LLM applications and agents. | Self-hosting brings database, retention, security, and upgrade responsibilities. | 2026-10-05 |
| [Ragas](https://github.com/vibrantlabsai/ragas) | Evaluation framework | Evaluating LLM applications, especially retrieval-augmented generation. | Automated metrics are proxies; combine them with human review and task ground truth. | 2026-10-05 |

### Deployment and operations

| Project | Type | Use it for | Tradeoff | Verified |
|---|---|---|---|---|
| [Kubernetes](https://github.com/kubernetes/kubernetes) | Orchestration platform | Scheduling and operating containerized workloads at scale. | Can be excessive for small applications; account for platform and team overhead. | 2026-10-05 |
| [Docker Compose](https://github.com/docker/compose) | Container tool | Defining and running multi-container applications, especially for development. | Not a universal substitute for production orchestration. | 2026-10-05 |
| [BentoML](https://github.com/bentoml/BentoML) | Model-serving platform | Packaging and serving inference APIs and AI workloads. | Test target hardware, model compatibility, and packaging assumptions. | 2026-10-05 |
| [Ray](https://github.com/ray-project/ray) | Distributed compute | Scaling distributed Python and machine-learning workloads. | Adds operational footprint; use when distributed execution is actually needed. | 2026-10-05 |
| [vLLM](https://github.com/vllm-project/vllm) | Inference engine | Serving supported language models with a high-throughput inference runtime. | Compatibility depends on model architecture, hardware, and runtime versions. | 2026-10-05 |

## Planned areas

These are areas to grow into—not claims of current completeness:

- End-to-end AI application patterns and tutorials
- Small, reproducible examples with clear setup and expected results
- Voice-agent evaluation and reporting (see [voice-agent-eval-corpus](https://github.com/shivamnegi92/voice-agent-eval-corpus))
- Deeper extraction and multimodal guides informed by [entity extraction](https://github.com/shivamnegi92/awesome-entity-extraction) and [multimodal extraction](https://github.com/shivamnegi92/awesome-multimodal-extraction)

Those linked repositories are separate projects with their own scopes and licenses. This catalog does not copy or automatically inherit their content.

## Origin and licensing policy

This catalog follows a deliberate project policy: **do not add China-origin models, vendors, or frameworks.** Origin is assessed for the project/vendor/model itself—not inferred from a contributor’s name or nationality. For ambiguous cases, do not list the resource until its origin is clear and the project policy is reviewed. This policy does not make claims about technical quality or people.

Project licenses vary. A catalog entry is not permission to reuse project code, model weights, or datasets. Check each upstream license and terms independently. The catalog’s original text is released under [CC0 1.0](LICENSE); third-party names and links remain with their respective owners.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before suggesting a project. We prioritize accurate, useful, maintainable entries over list size. Corrections to this policy or its scope are welcome through a GitHub issue or pull request.

## Scope and status

This is an early, human-curated catalog. GitHub links and public project status were checked on **2026-10-05**; entries have not all been installed or independently benchmarked. Re-check upstream documentation, release status, security, and licensing before adoption. The catalog is not exhaustive, and inclusion is not a quality, safety, or legal endorsement.

<!-- TRENDING-CATALOG:START -->


## Recently reviewed discoveries

> Candidates below were discovered from the cited trend/source observation and reviewed for this catalog. Popularity is a discovery signal, not a quality ranking.

### Agents and orchestration

| Project | Practical use | Tradeoff |
|---|---|---|
| [Browser Use](https://github.com/browser-use/browser-use) | Build agents that interact with websites through browser automation. | The project evolves quickly and now coexists with hosted commercial services; verify the pinned version, security boundaries, and service terms for your use case. |

<!-- Discovery records: catalog/trend-sources.json -->
<!-- TRENDING-CATALOG:END -->
