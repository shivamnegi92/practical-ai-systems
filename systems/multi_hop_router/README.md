# Multi-hop reasoning router

Split a multi-part question into sub-questions, answer each independently with this system's bundled BM25/extractive baseline, and abstain overall unless every part is answered.

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

See [`eval/results.json`](eval/results.json) for abstention accuracy on ten synthetic questions. The shared Python/TypeScript question-and-gold matrix preserves both original question variants, adds single-hop and multi-hop answerable controls, and includes two unsupported qualifiers. Neither port's bundled facts specify an Enterprise price or a euro-denominated Pro price. Python returns the dollar Pro price for both; TypeScript abstains on Enterprise but returns the dollar price for the euro question. Correct gold labels retain these failures: **8/10 in Python and 9/10 in TypeScript**.

Python reads this system's own `data` Markdown files, and TypeScript uses its own inline `CHUNKS`. The full corpora are not identical; the fixture labels concern facts common to both or absent from both. Retrieval thresholds, splitting and answering remain unchanged. The metric checks only the abstention decision, not answer completeness, numeric correctness or entailment.

## Known limitations

- Decomposition is a regex split on " and " or a mid-string "?"; genuinely compound questions phrased without those connectors will not be split and may be answered (or abstained) incorrectly as a single unit.
- Lexical coverage does not verify qualifiers or entailment: an answer can overlap a question while missing its requested plan or currency.
- All-or-nothing abstention means one unanswerable sub-question blocks the whole response, even when the other parts have solid answers.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
