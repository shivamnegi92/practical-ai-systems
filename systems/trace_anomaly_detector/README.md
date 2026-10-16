# Trace anomaly detector

Flag anomalous execution-trace durations with a z-score against a historical baseline, plus an explicit error flag.

**Level:** advanced · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.trace_anomaly_detector.evaluate
```

## Evaluate and test

```bash
python3 -m systems.trace_anomaly_detector.evaluate
python3 -m unittest systems.trace_anomaly_detector.test_anomaly
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current precision/recall on 4 synthetic traces scored against a 10-point baseline: a normal duration, a large spike, an error-flagged fast trace, and a borderline-but-normal duration.

## Known limitations

- Durations and the z-score threshold must be numeric, finite and nonnegative; invalid inputs raise an error before scoring instead of producing NaN or an apparent normal result. Zero and fractional values remain allowed. This does not add statistical confidence, validate record shape, or change missing/constant-baseline behavior.

- A 10-point baseline is far too small to estimate a stable mean/standard deviation for any real service; this is illustrative, not production-grade statistics.
- The z-score threshold (3.0) assumes a roughly normal distribution of durations, which real latency data rarely is (it's typically right-skewed).
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
