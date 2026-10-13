# RAG citation support checker

Verify that each inline `[chunk_id]` citation in a generated answer is lexically supported by the chunk it points to.

**Level:** intermediate · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.citation_checker.evaluate
```

## Evaluate and test

```bash
python3 -m systems.citation_checker.evaluate
python3 -m unittest systems.citation_checker.test_citation_checker
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current citation-status accuracy on 8 synthetic citations, including changed amounts, dates and percentages plus matching-value controls. The original 5-minutes/60-seconds claim is now correctly labelled unsupported rather than accepted for lexical similarity.

## Known limitations

- Each claim's literal numeric tokens (including currency markers, decimal/grouping separators, dates and percentages) must occur in its cited source, otherwise the result is unsupported with `number_mismatch`. Citation IDs are excluded from this check. This is token presence, not entailment: matching values can still describe the wrong thing, and equivalent numeric/date/currency formats can be rejected. Values split across multiple cited sources are not combined.
- The 0.3 overlap threshold is an arbitrary cutoff picked for this fixture, not a calibrated groundedness score.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
