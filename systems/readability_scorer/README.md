# Readability grade scorer

Estimate a Flesch-Kincaid-style reading grade level and bucket it into simple/standard/complex. No external NLP library.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.readability_scorer.app "The cat sat on the mat. It was a hot day."
```

## Evaluate and test

```bash
python3 -m systems.readability_scorer.evaluate
python3 -m unittest systems.readability_scorer.test_readability
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current band accuracy on 4 synthetic texts spanning simple, standard, and complex writing.

## Known limitations

- Calculated grades are clamped to zero to keep the numeric API and avoid a negative grade for very short text such as `Hi`. Empty or punctuation-only input also returns zero. Short samples still give unreliable estimates; zero is a display floor, not a validated learning level.

- Syllable counting is a vowel-run heuristic, not a dictionary or phoneme model; it will misjudge many real words (silent letters, diphthongs, compound words).
- The simple/standard/complex cutoffs (6 and 12) are arbitrary bucket boundaries chosen for this fixture, not a validated pedagogical standard.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
