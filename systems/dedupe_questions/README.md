# Near-duplicate question detector

Flag probable duplicate support questions with token Jaccard similarity, no embeddings required.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.dedupe_questions.app "How do I reset my password?" "How can I reset my password?"
```

## Evaluate and test

```bash
python3 -m systems.dedupe_questions.evaluate
python3 -m unittest systems.dedupe_questions.test_dedupe
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current precision/recall on 5 handcrafted question pairs at a 0.6 similarity threshold.

## Known limitations

- The duplicate threshold must be a numeric proportion from 0 through 1. Invalid/non-finite thresholds are rejected even with no question pairs. The Python CLI reports an argument error instead of silently calling identical questions different; valid boundary/default behavior is unchanged.

- Jaccard similarity over stemmed tokens cannot tell "refund" from "return" apart, and it cannot detect duplicates phrased with completely different words.
- The 0.6 threshold is an arbitrary cutoff picked for this fixture; retune it against your own labeled pairs before reuse.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
