# Multi-agent triage handoff

Route a request through a triage step to the right specialist, escalating to a human when confidence is low or the category is unclear.

**Level:** advanced · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.multi_agent_handoff.app "There is a refund issue with my invoice payment."
```

## Evaluate and test

```bash
python3 -m systems.multi_agent_handoff.evaluate
python3 -m unittest systems.multi_agent_handoff.test_handoff
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current handoff accuracy on 4 synthetic requests: two clear category matches that resolve, one off-topic request, and one single-keyword request that is too thin to route confidently.

## Known limitations

- Equal best keyword scores are ambiguous: triage returns a `null` category and keeps the top score for inspection; the request escalates even when the score meets the threshold. A unique winner still uses the existing threshold.

- Triage is a fixed keyword-overlap scorer over three hand-picked categories; anything phrased without those words escalates even when a human would route it instantly.
- The confidence threshold (2 keyword matches) is an arbitrary cutoff for this fixture, not a calibrated confidence score.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
