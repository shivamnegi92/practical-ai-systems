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

This measured BM25 retrieval coverage, extractive sentence coverage, citation matching, and answerable/unanswerable abstention on a shared Python/web matrix of 26 handcrafted synthetic questions (the original 22 Python cases and five-case web subset remain). It did not use a model, external docs, human raters, or production traffic. The small fixture only checks regressions; it does not support general quality claims. See [`eval/results.json`](eval/results.json) and [`eval/cases.json`](eval/cases.json).

- Retrieval recall@3: **1.00**
- Extracted sentence includes expected fact: **0.89**
- Citation points to labeled source chunk: **0.94**
- Correct abstention on unanswerable questions: **0.75**

## Known limitations

- High lexical overlap returns a current-dollar sentence for a yen-denominated question in Python, or unrelated Pro text for a future-year price in both ports. The web port correctly abstains on the yen question; it scores 7/8 (0.875) correct abstentions versus Python 6/8 (0.75) on the same eight unsupported questions. Existing tokenization/coverage differences are measured, not tuned away. The source contains neither yen pricing nor 2035 prices, so these new gold labels require abstention. Two other unsupported-qualifier cases (Enterprise history and reset validity after five failed attempts) correctly abstain. No runtime thresholds, corpus or model behavior were changed.

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
