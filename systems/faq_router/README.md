# FAQ intent router

Route a short support message to one of five fixed intents (or "unknown") using keyword overlap.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.faq_router.app "I want to cancel my subscription"
```

## Evaluate and test

```bash
python3 -m systems.faq_router.evaluate
python3 -m unittest systems.faq_router.test_router
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current routing accuracy on 8 synthetic messages, including charged-twice/log-in cases, a tied-keyword case and an off-topic fallback case.

## Known limitations

- Queries and keywords share a simple suffix/silent-e normalization heuristic; this is not a general morphological analyzer. Multi-word keywords such as `log in` match consecutive tokens in order, including stopwords. Normalized duplicate keywords count once; phrase and single-word matches can still overlap.

- Intents are a fixed, hand-picked keyword list; anything phrased without those words routes to "unknown" even when a human would understand it immediately.
- Ties between intents resolve to whichever intent is checked first, which is an arbitrary order, not a confidence ranking.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
