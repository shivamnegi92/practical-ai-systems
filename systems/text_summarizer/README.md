# Extractive text summarizer

Pick the most representative sentences from a short document using word-frequency scoring. No model, no API key.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.text_summarizer.app "Database indexing speeds up queries. Indexing indexing indexing is crucial for performance. The weather was nice yesterday." --n 1
```

## Evaluate and test

```bash
python3 -m systems.text_summarizer.evaluate
python3 -m unittest systems.text_summarizer.test_summarizer
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for the current numbers on 6 handcrafted fixtures: five repeat a topic word three times, and one preserves a sentence containing Dr. and p.m.

## Known limitations

- The sentence splitter protects a fixed, case-insensitive list: Dr., Mr., Mrs., Ms., e.g., i.e., a.m., p.m., etc. It will miss other abbreviations and cannot determine when a listed abbreviation also ends a sentence. This is a small heuristic rather than a full language-aware segmenter.

- Scoring is a plain term-frequency average; it has no notion of meaning, coreference, or discourse structure, so it can pick a sentence that repeats a word without actually being the most important one.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- Read the source, evaluation case file, and printed method/scope before reusing.
