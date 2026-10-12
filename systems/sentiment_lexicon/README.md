# Lexicon-based sentiment classifier

Classify short text as positive, negative, or neutral using a small hand-built word list. No model, no training data.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.sentiment_lexicon.app "This product is great and the support team is fantastic."
```

## Evaluate and test

```bash
python3 -m systems.sentiment_lexicon.evaluate
python3 -m unittest systems.sentiment_lexicon.test_sentiment
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current accuracy on 7 synthetic sentences, including not-good/not-bad negation cases and one mixed-sentiment case that intentionally ties and falls back to neutral.

## Known limitations

- Negation flips a lexicon word when any of `not`, `never`, `no`, or an `n't` contraction occurs in the previous three word tokens. This scope heuristic ignores syntax, punctuation boundaries, and double negation; for example, "I don't think it's bad" may not express the polarity it assigns. There is no stemming, so inflections outside the hard-coded list remain invisible.
- Ties between positive and negative word counts always resolve to neutral, which is a crude tie-break, not a confidence-aware decision.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
