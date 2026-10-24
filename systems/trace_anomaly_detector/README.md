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

See [`eval/results.json`](eval/results.json) for current precision/recall on 10 synthetic traces: the original four variable-baseline cases plus constant/zero-mean baselines, the reported 100x spike, and tolerance controls.

## Known limitations

- For a nonempty baseline with zero standard deviation, a duration is anomalous only when its absolute deviation is strictly greater than 50% of the absolute mean. Equality stays normal; a zero mean flags any nonzero deviation. Empty history supplies no latency inference, but explicit error flags still apply. This deterministic fallback avoids inventing a standard deviation; `z_score` remains the existing 0 placeholder and is not evidence of normality in these cases.

- A 10-point baseline is far too small to estimate a stable mean/standard deviation for any real service; this is illustrative, not production-grade statistics.
- The z-score threshold (3.0) assumes a roughly normal distribution of durations, which real latency data rarely is (it's typically right-skewed).
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
