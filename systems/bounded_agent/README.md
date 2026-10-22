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

All **10** policy fixtures pass in the shared Python/TypeScript matrix. The original three cases remain; web demonstration requests, approval true/false controls, malformed array/string arguments and another disallowed action expand the refusal side. Approved lookup/refund controls and two unapproved refunds distinguish permission from approval. The existing web demonstration fields are preserved alongside case counts and policy accuracy. This measures only deterministic policy enforcement, not model planning or real tool integration. Do not connect side-effectful tools without authorization, audit logs, and stronger boundary tests. See [`eval/results.json`](eval/results.json).

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- Status-only evaluation uses stub tools and plans created by `plan()`. It does not test forged plan objects, real identity/approval authentication, argument schemas for individual tools, or side-effect execution. Refusal controls are abstention cases; no newly discovered runtime failure or exhaustive security coverage is claimed.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
