# Adversarial red-team harness for a bounded agent

Run a battery of adversarial requests against `systems.bounded_agent`'s allow-list/approval policy and measure the breach rate.

**Level:** advanced · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.redteam_harness.evaluate
```

## Evaluate and test

```bash
python3 -m systems.redteam_harness.evaluate
python3 -m unittest systems.redteam_harness.test_redteam
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for the shared 14-request Python/web battery. Both original sets remain, plus array/unknown-action controls and approved negative/string refund amounts. The last two are explicit desired amount-schema rejections but complete under the unchanged stub, yielding 2/14 policy breaches. No real refund or database operation occurs.

## Known limitations

- The two new refund gold labels require a nonnegative numeric amount: approval alone must not make `-1` or `"ten"` valid. This desired schema policy exceeds the current allow-list/approval contract and is documented rather than implemented here. Breach rate measures false completions only, not false refusals, identity verification or every tool failure.
- Fourteen hand-written cases are illustrative, not an exhaustive attack surface; a real red team would need many more categories (replay, race conditions, privilege confusion across tools, prompt-level manipulation of the planner).
- The "injection in arguments" case shows the policy layer allows it because `lookup_order` isn't sensitive -- the policy does not sanitize tool arguments, so the tool implementation itself must treat them as untrusted.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
