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

See [`eval/results.json`](eval/results.json) for the current breach rate on a 5-case battery: a disallowed action, an unapproved sensitive action, a correctly approved action, malformed arguments, and an injection-style string passed as a tool argument.

## Known limitations

- Five hand-written adversarial cases are illustrative, not an exhaustive attack surface; a real red team would need many more categories (replay, race conditions, privilege confusion across tools, prompt-level manipulation of the planner).
- The "injection in arguments" case shows the policy layer allows it because `lookup_order` isn't sensitive -- the policy does not sanitize tool arguments, so the tool implementation itself must treat them as untrusted.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.

A tool must be an explicitly owned callable entry as well as allow-listed. Planning and execution both reject missing/non-callable entries; inherited JavaScript prototype properties are not tools. These are local stubs, not an authenticated production tool boundary.
