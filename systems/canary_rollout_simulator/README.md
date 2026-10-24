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

See [`eval/results.json`](eval/results.json) for current decision accuracy on 7 synthetic scenarios: the original promote/rollback cases plus zero/missing baseline holds, zero-on-zero and known-error controls.

## Known limitations

- A missing or nonpositive baseline p95 cannot define a percentage regression. The comparison returns `hold` with `missing_latency_baseline` and a null percentage, rather than promoting on a fabricated zero. A known error-rate regression still returns `rollback`. This conservative pause does not establish a valid baseline; collect representative measurements before deciding.

- This is a two-sample point comparison against fixed thresholds, not a statistical test; it has no concept of sample size, variance, or confidence, and will over-react to noisy small samples.
- Guardrail thresholds (2% error delta, 20% latency regression) are illustrative constants, not values validated against any real service.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
