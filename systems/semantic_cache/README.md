# Exact-response cache

Cache exact normalized requests with model-key isolation, TTL, and bounded LRU. Similar paraphrases deliberately miss.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.semantic_cache.evaluate
```

## Evaluate and test

```bash
python3 -m systems.semantic_cache.evaluate
python3 -m unittest systems.semantic_cache.test_cache
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

Exact replay is **6/6** across six synthetic queries. Two additional lookups exercise an apostrophe/punctuation hit and a price/prize miss. The illustrative two-pass workload would avoid 50% duplicate calls only because it intentionally repeats every exact query once; this is not an observed production savings claim. Paraphrases miss by design. See [`eval/results.json`](eval/results.json).

## Known limitations

- Apostrophes are removed and other Unicode punctuation becomes whitespace before keying; word boundaries are preserved. This heuristic can conflate punctuation-bearing meanings, so it is unsuitable for queries where punctuation changes the answer. Model/version keys are unchanged.

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
