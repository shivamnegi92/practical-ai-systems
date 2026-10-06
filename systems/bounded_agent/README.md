# Approval-gated tool workflow

Run allow-listed tools with typed inputs and explicit approval gates for side effects.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.bounded_agent.evaluate
```

## Evaluate and test

```bash
python3 -m systems.bounded_agent.evaluate
python3 -m unittest systems.bounded_agent.test_agent
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

All **3** policy fixtures pass: an allowed lookup, an unapproved refund that must pause, and a disallowed delete. This measures only deterministic policy enforcement, not model planning or real tool integration. Do not connect side-effectful tools without authorization, audit logs, and stronger boundary tests. See [`eval/results.json`](eval/results.json).

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
