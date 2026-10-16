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

See [`eval/results.json`](eval/results.json) for current breach-decision accuracy across 3 synthetic scenarios: a latency spike, a within-budget log, and a cost-only breach.

## Known limitations

- Summaries and budget decisions reject nonnumeric, Boolean, negative and nonfinite measurements/limits with `ValueError` (Python) or `RangeError` (TypeScript). Token counts must be integral; omitted tokens default to zero. Zero and empty logs remain valid. Aggregation that produces a nonfinite result is also rejected, so invalid data cannot yield an apparently clean budget verdict.

- This is a fixed two-threshold guardrail, not a statistical anomaly test; it does not account for sample size, noise, or seasonal traffic patterns.
- Percentiles are computed with linear interpolation over the whole provided batch, not a streaming or windowed estimate.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
