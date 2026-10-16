# Multi-hop reasoning router

Split a multi-part question into sub-questions, answer each independently with `systems.doc_qa`, and abstain overall unless every part is answered.

**Level:** advanced · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.multi_hop_router.app "How much does the Pro plan cost and how often do notes sync?"
```

## Evaluate and test

```bash
python3 -m systems.multi_hop_router.evaluate
python3 -m unittest systems.multi_hop_router.test_multi_hop
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current abstention accuracy on 3 synthetic multi-part questions over `systems/doc_qa`'s bundled documents: two fully-answerable questions and one with an unanswerable second part.

## Known limitations

- Decomposition is a regex split on " and " or a mid-string "?"; genuinely compound questions phrased without those connectors will not be split and may be answered (or abstained) incorrectly as a single unit.
- All-or-nothing abstention means one unanswerable sub-question blocks the whole response, even when the other parts have solid answers.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.

The internal BM25 search count `k` must be a nonnegative integer. Zero returns no hits; negative, fractional and non-finite counts are rejected before searching, including empty indexes. Wrapper-specific default/clamping policies remain unchanged.
