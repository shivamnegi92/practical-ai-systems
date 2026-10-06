# Lexical retrieval baseline

A tiny, deterministic retrieval baseline you can run and inspect without an API key, model download, or third-party dependency. It exists to give a document-search project a measurable starting point before adding embeddings, rerankers, or generation.

## Run it

From the repository root:

```bash
python3 - <<'PY'
from examples.lexical_retrieval_baseline.retrieve import rank_documents

documents = {
    "leave-policy": "Employees can request parental leave through the HR portal.",
    "store-hours": "The store opens at eight in the morning.",
}

print(rank_documents("How do I request parental leave?", documents, top_k=2))
PY
```

Example output:

```text
[('leave-policy', 0.5)]
```

The score is the fraction of unique query terms present in the document. It is not a probability or relevance confidence.

## Run tests

```bash
python3 -m unittest -v examples.lexical_retrieval_baseline.test_retrieve
```

## Method

- Tokenize lowercase ASCII letters/digits using a small regular expression.
- Compare unique query tokens with unique document tokens.
- Score each matching document as `overlap_count / unique_query_token_count`.
- Omit documents with no query-token overlap.
- Sort scores descending; break ties by document ID for stable output.

## What this baseline cannot do

- Understand synonyms, paraphrases, morphology, or word meaning.
- Handle multilingual tokenization, phrase structure, or complex identifiers.
- Score term rarity, document length, field weights, or recency.
- Apply permissions, filters, or document-version rules.

Use it to test the data path and make retrieval failures visible—not as a claim of semantic search quality. Extend one limitation at a time and keep the same labeled query set for comparison.

## Evaluation exercise

Create a small file with realistic queries, relevant document IDs, and deliberately unanswerable cases. For each query, inspect the top-k results and record whether relevant evidence appears. Compare this lexical baseline with any next retrieval design under the same corpus snapshot and query set. See the [evaluation playbook](../../benchmarks/README.md) and [document-search recipe](../../recipes/document-search/README.md).
