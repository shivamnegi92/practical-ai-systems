# Information extraction and document AI

> Turn text and documents into structured, usable data.

[← Back to Practical AI Systems](../README.md)

## Catalog

Records are metadata-reviewed, not blanket endorsements.

| Project | What it does | Best for | Tradeoffs to consider | Delivery | License | Evidence |
|---|---|---|---|---|---|---|
| [Apache Tika](https://github.com/apache/tika) | Detect file types and extract text and metadata from a broad range of formats. | content detection and baseline text/metadata extraction; building blocks for ingestion | A parser toolkit is not a complete layout-aware document-understanding pipeline. | library, tool | Apache-2.0 | metadata-reviewed |
| [Docling](https://github.com/docling-project/docling) | Parse and convert complex documents into structured representations for downstream applications. | document ingestion; layout-aware conversion before retrieval or extraction | Validate parsing quality on representative file types, languages, and layouts from your own corpus. | library, tool | MIT | metadata-reviewed |
| [MarkItDown](https://github.com/microsoft/markitdown) | Convert files and office documents into Markdown for downstream text workflows. | lightweight document-to-text conversion; prototyping text-centric ingestion | Markdown conversion can lose layout or semantic relationships needed for precise extraction. | library, tool | MIT | metadata-reviewed |
| [Unstructured](https://github.com/Unstructured-IO/unstructured) | Ingest and partition diverse file formats into structured elements for downstream workflows. | multi-format document ingestion; document pipelines that need a common representation | Check which connectors and capabilities are open source versus hosted or commercial. | library, service | Apache-2.0 | metadata-reviewed |

## Choosing well

Start with the smallest component that solves the job. Validate it with your data, constraints, and failure cases before expanding the architecture.
