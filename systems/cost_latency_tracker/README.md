# Cost and latency guardrail tracker

Summarize a request log into p50/p95 latency and cost, then flag budget breaches against configured thresholds.

**Level:** intermediate · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.cost_latency_tracker.evaluate
```

## Evaluate and test

```bash
python3 -m systems.cost_latency_tracker.evaluate
python3 -m unittest systems.cost_latency_tracker.test_tracker
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for breach-decision accuracy across ten synthetic scenarios shared with TypeScript, retaining the three original scenarios and the web demonstration. Controls cover exact threshold equality (strict `>`), both breaches, empty logs and absent token counts. Empty-log labels describe the current zero-summary behavior, not evidence that a service is healthy.

Two desired raw-threshold cases remain failures under unchanged budget logic: cost `0.00004` exceeds `0.00003` but the displayed total rounds to zero; p95 latency `100.004` exceeds `100.002` but rounds to `100.00`. Gold labels explicitly apply thresholds to unrounded values, beyond the current rounded-summary comparison. Both ports score **8/10**. This documents the limitation without changing budget policy. The web demo summary and budget fields remain available.

## Known limitations

- This is a fixed two-threshold guardrail, not a statistical anomaly test; it does not account for sample size, noise, or seasonal traffic patterns.
- Budget comparisons use rounded summary values (two decimals for latency and four for cost), so sufficiently small raw-value crossings can be missed.
- Percentiles are computed with linear interpolation over the whole provided batch, not a streaming or windowed estimate.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
