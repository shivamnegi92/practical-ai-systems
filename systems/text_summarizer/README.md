# Extractive text summarizer

The sentence count `n` must be a nonnegative integer. Zero produces an empty summary; a count larger than the available sentences returns them all. Invalid counts raise an error even for empty or short input.

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

See [`eval/results.json`](eval/results.json) for the current numbers on 5 handcrafted fixtures, each designed so one sentence repeats a topic word three times.

## Known limitations

- Scoring is a plain term-frequency average; it has no notion of meaning, coreference, or discourse structure, so it can pick a sentence that repeats a word without actually being the most important one.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- Read the source, evaluation case file, and printed method/scope before reusing.
