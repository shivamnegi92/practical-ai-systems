# Retrieval evaluation harness

Score a retrieval strategy with recall@k, MRR, and nDCG@k, and compare a baseline against a synonym-expanded run side by side.

**Level:** advanced · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.retrieval_eval_harness.evaluate
```

## Evaluate and test

```bash
python3 -m systems.retrieval_eval_harness.evaluate
python3 -m unittest systems.retrieval_eval_harness.test_harness
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json). This reuses the four-query, four-document fixture from `systems/query_rewriter` and reports recall@k/MRR/nDCG@k for both the plain BM25 baseline and the synonym-expanded run from that system.

## Known limitations

- Four queries over four documents with binary relevance is enough to illustrate the metrics, not enough to generalize a strategy comparison.
- nDCG here uses binary or small integer relevance grades supplied by hand; it is only as trustworthy as those judgments.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.

The internal BM25 search count `k` must be a nonnegative integer. Zero returns no hits; negative, fractional and non-finite counts are rejected before searching, including empty indexes. Wrapper-specific default/clamping policies remain unchanged.
