# Document Q&A with citations

Search documentation with lexical retrieval, extractive answers, citations, and abstention.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.doc_qa.app "How much does Pro cost?"
```

## Evaluate and test

```bash
python3 -m systems.doc_qa.evaluate
python3 -m unittest systems.doc_qa.test_doc_qa
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

This measured BM25 retrieval coverage, extractive sentence coverage, citation matching, and answerable/unanswerable abstention on 22 handcrafted synthetic questions. It did not use a model, external docs, human raters, or production traffic. The small fixture only checks regressions; it does not support general quality claims. See [`eval/results.json`](eval/results.json) and [`eval/cases.json`](eval/cases.json).

- Retrieval recall@3: **1.00**
- Extracted sentence includes expected fact: **0.89**
- Citation points to labeled source chunk: **0.94**
- Correct abstention on unanswerable questions: **1.00**

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
