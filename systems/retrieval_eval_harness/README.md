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

See [`eval/results.json`](eval/results.json). The shared eleven-query matrix preserves both original sets and adds two multi-relevant judgments plus two unmatched synonym intents. It reports recall@3, MRR and nDCG@3 on the original separate corpora: Python has weather/generic deletion, web has shipping/account deletion. These are different corpus conditions, not an identical strategy comparison across ports.

## Known limitations

- `business day` has both cancellation/deletion targets: Python retrieves both, but the web deletion chunk lacks the phrase, yielding 0.5 recall. `membership tariff` and `end subscription` fail even after expansion in both ports. Original runtime, corpora, synonym dictionary and binary relevance metrics remain unchanged.
- Eleven queries over four documents with binary relevance is enough to illustrate the metrics, not enough to generalize a strategy comparison.
- nDCG here uses binary or small integer relevance grades supplied by hand; it is only as trustworthy as those judgments.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
