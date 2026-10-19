// Flag anomalous trace durations using z-scores against a historical baseline.
// A trace is flagged when it carries an explicit error flag, or when its
// duration is more than `zThreshold` standard deviations from the baseline mean.

function mean(values: number[]): number {
  return values.length ? values.reduce((a, b) => a + b, 0) / values.length : 0;
}

function stdev(values: number[]): number {
  if (values.length < 2) return 0;
  const m = mean(values);
  const variance = values.reduce((sum, v) => sum + (v - m) ** 2, 0) / (values.length - 1);
  return Math.sqrt(variance);
}

export interface Trace {
  name: string;
  duration_ms: number;
  error?: boolean;
}

export function detectAnomalies(baseline: number[], traces: Trace[], zThreshold = 3.0) {
  if (typeof zThreshold !== "number" || Number.isNaN(zThreshold) || zThreshold <= 0) {
    throw new RangeError(`zThreshold must be a positive number, got ${zThreshold}`);
  }
  const baselineMean = mean(baseline);
  const baselineSd = stdev(baseline);
  return traces.map((trace) => {
    const z = baselineSd ? (trace.duration_ms - baselineMean) / baselineSd : 0;
    const anomalous = Boolean(trace.error) || Math.abs(z) > zThreshold;
    return { name: trace.name, z_score: Math.round(z * 100) / 100, anomalous };
  });
}

export const BASELINE = [100, 105, 98, 102, 97, 101, 103, 99, 100, 104];
export const TRACES: Trace[] = [
  { name: "normal-1", duration_ms: 101 },
  { name: "normal-2", duration_ms: 96 },
  { name: "slow-outlier", duration_ms: 400 },
  { name: "flagged-error", duration_ms: 100, error: true },
];
const GOLD_ANOMALOUS = [false, false, true, true];

export function evaluateAll() {
  const results = detectAnomalies(BASELINE, TRACES);
  let tp = 0, fp = 0, fn = 0, tn = 0;
  results.forEach((r, i) => {
    if (r.anomalous && GOLD_ANOMALOUS[i]) tp++;
    else if (r.anomalous && !GOLD_ANOMALOUS[i]) fp++;
    else if (!r.anomalous && GOLD_ANOMALOUS[i]) fn++;
    else tn++;
  });
  const precision = tp + fp ? tp / (tp + fp) : 0;
  const recall = tp + fn ? tp / (tp + fn) : 0;
  const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
  return { cases: TRACES.length, precision, recall, f1 };
}
