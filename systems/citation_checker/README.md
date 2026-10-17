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

See [`eval/results.json`](eval/results.json) for current citation-status accuracy on a 4-citation synthetic answer: two correct citations, one fabricated claim, and one citation pointing to a chunk that doesn't exist.

## Known limitations

- Citation marker text is removed before scoring claim vocabulary. Renaming a chunk ID cannot supply or dilute evidence, and a marker-only sentence is unsupported even at threshold zero. Original annotated sentences remain in reports.
- Removing marker dilution exposes a remaining browser false positive: the unsupported video-call claim shares `pro` and `plan` with the source and meets the unchanged 0.3 threshold. Browser fixture accuracy is now **0.75**, with unchanged gold labels; this is an honest limitation, not a claim that the fabricated answer became valid.

- Token overlap cannot catch numeric or factual fabrication when the surrounding vocabulary still matches (e.g., "every 5 minutes" vs. the source's "every 60 seconds" both pass as lexically supported here).
- The 0.3 overlap threshold is an arbitrary cutoff picked for this fixture, not a calibrated groundedness score.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
