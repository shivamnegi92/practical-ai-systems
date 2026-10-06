# Document search: build a retrieval baseline before adding agents

A document assistant is only as useful as the evidence it can retrieve. Start with a retrieval system you can measure; add generation after you can tell whether the right passages are being found.

## Good fit

Use this path when people need answers from a bounded collection of PDFs, policies, manuals, or other documents, and they need citations back to those sources.

Do not start here if the task is a conventional database lookup, if documents are not legally available to process, or if the answer must come from authoritative structured records that can be queried directly.

## Baseline architecture

```text
Documents → parse + provenance → chunk → index → retrieve → inspect evidence
                                                        ↓
                                              answer + citations (later)
```

Keep source identity, page/section, version, and access-control metadata attached throughout ingestion. If access control is lost during indexing, retrieval may leak content even when the source system was secure.

## Build the smallest useful baseline

1. **Define the task.** Write 20–50 representative questions and identify which source passages support each answer. Include unanswerable questions.
2. **Inspect your corpus.** Check file types, scan quality, tables, languages, duplicates, freshness, and permission boundaries.
3. **Parse with provenance.** Record source URL or ID, document version, page/section, and extraction warnings. Preserve originals outside the index.
4. **Start with lexical retrieval.** A text search baseline gives you a useful floor and makes failures easier to inspect.
5. **Add vector or hybrid retrieval only with a reason.** Evaluate semantic recall against lexical search; tune chunk boundaries and filters using real queries.
6. **Show retrieved passages before generating answers.** Review whether relevant evidence is present, correctly attributed, and permitted for the user.
7. **Add generation with citations.** Require source references in output and make “not found” an acceptable outcome.
8. **Measure failures separately.** Retrieval missed evidence, parser corrupted a table, permissions filtered the answer, or the generator ignored evidence? These are different bugs.

## Minimum evaluation set

For each query, keep a small labeled set of relevant document spans. Track:

- **Recall@k:** did retrieval include relevant evidence in its top-k results?
- **Precision@k:** how much of the returned material was relevant?
- **Citation correctness:** does each cited page/section actually support the claim?
- **Abstention behavior:** does the system avoid inventing answers when evidence is absent?
- **Access-control correctness:** can a user retrieve only what they are allowed to see?
- **Latency and cost:** measure indexing and query stages separately.

Record corpus snapshot, parser/index versions, chunking parameters, retrieval settings, and evaluator version with each run. A score without these is not a reproducible comparison.

## Common failure modes

- OCR silently drops a table column or reading order.
- Chunking separates a value from the heading that gives it meaning.
- Duplicate or superseded documents dominate results.
- A global vector index ignores user-level permissions.
- The generator cites a nearby passage that does not entail its answer.
- One aggregate score hides failures by language, file type, or business unit.

## Choosing components

Browse [retrieval and knowledge systems](../../catalog/retrieval.md) for indexing/retrieval options and [document AI](../../catalog/extraction.md) for parsing tools. Compare them on your own corpus, not on a vendor demo. Keep the parser, retriever, generator, and evaluator separable until your evidence justifies coupling them.
