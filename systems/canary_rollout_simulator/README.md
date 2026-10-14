# Canary rollout simulator

Compare canary metrics against a baseline using fixed error-rate and latency guardrails to decide promote or rollback.

**Level:** advanced · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.canary_rollout_simulator.evaluate
```

## Evaluate and test

```bash
python3 -m systems.canary_rollout_simulator.evaluate
python3 -m unittest systems.canary_rollout_simulator.test_canary
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for decision accuracy on twelve synthetic scenarios shared with TypeScript: both original Python/web matrices, exact 2% error-delta and 20% latency boundaries, simultaneous regressions, improvements and two invalid-rate cases.

The latter gold labels explicitly describe a desired fail-closed policy: hold when the baseline rate is negative or the canary rate exceeds one, since such inputs are not valid error proportions. The current runtime does not validate these values and instead chooses promote/rollback, so both remain failures (10/12 correct). This is a documented evaluation policy beyond current behavior, not an algorithm change or a universally validated rollout policy. The zero/missing baseline fix is handled separately by PR #32; this evaluation does not duplicate those cases.

## Known limitations

- This is a two-sample point comparison against fixed thresholds, not a statistical test; it has no concept of sample size, variance, or confidence, and will over-react to noisy small samples.
- Invalid error rates are not rejected or held; point comparisons can produce a definite decision on nonsensical aggregates.
- Guardrail thresholds (2% error delta, 20% latency regression) are illustrative constants, not values validated against any real service.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
