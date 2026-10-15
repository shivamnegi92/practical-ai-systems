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

See [`eval/results.json`](eval/results.json) for status and category-aware accuracy on the shared 13-request Python/web matrix. Both original sets remain; repeated-keyword and empty controls pass. Two cross-category ties should escalate under the new explicit desired ambiguity policy, but the unchanged runtime resolves both. It scores 11/13 on both measures.

## Known limitations

- Equal best scores are broken by category insertion order. The added gold policy requires escalation with no unique destination when billing/technical or account/technical each score two. This stricter desired policy is documented, not implemented here. Repeating one keyword still counts as one; the confidence field is a count, not a probability.
- Triage is a fixed keyword-overlap scorer over three hand-picked categories; anything phrased without those words escalates even when a human would route it instantly.
- The confidence threshold (2 keyword matches) is an arbitrary cutoff for this fixture, not a calibrated confidence score.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
