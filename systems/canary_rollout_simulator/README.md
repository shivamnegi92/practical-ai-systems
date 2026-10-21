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

See [`eval/results.json`](eval/results.json) for current decision accuracy on 3 synthetic scenarios: a within-guardrail promote, an error-rate spike, and a latency regression.

## Known limitations

- Configured regression limits must be finite nonnegative numbers, with Boolean/string values rejected (`ValueError`/`RangeError`). Zero means no regression is allowed; deliberately relaxed finite limits remain valid. This validates configuration, separately from unavailable/invalid baseline or canary metrics.

- This is a two-sample point comparison against fixed thresholds, not a statistical test; it has no concept of sample size, variance, or confidence, and will over-react to noisy small samples.
- Guardrail thresholds (2% error delta, 20% latency regression) are illustrative constants, not values validated against any real service.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
