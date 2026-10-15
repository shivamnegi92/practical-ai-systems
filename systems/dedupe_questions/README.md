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

See [`eval/results.json`](eval/results.json) for current precision/recall on a shared 13-pair Python/web matrix (both original matrices retained) at a 0.6 similarity threshold.

## Known limitations

- Added gold labels distinguish enabling from disabling/not enabling alerts and account recovery from deletion. Synonymous password-change and notification questions should deduplicate, but token overlap can miss them. A case/punctuation control retains an easy true positive. No runtime or threshold tuning is included.
- Jaccard similarity over stemmed tokens cannot tell "refund" from "return" apart, and it cannot detect duplicates phrased with completely different words.
- The 0.6 threshold is an arbitrary cutoff picked for this fixture; retune it against your own labeled pairs before reuse.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
