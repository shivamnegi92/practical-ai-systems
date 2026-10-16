// Two-sample canary vs. baseline guardrail check for a promote/rollback decision.
// A fixed-threshold comparison, not a statistically rigorous A/B test: it
// ignores sample size, variance, and confidence intervals.

export interface Metrics {
  error_rate: number;
  p95_latency_ms: number;
}

export function decide(
  baseline: Metrics,
  canary: Metrics,
  maxErrorRateDelta = 0.02,
  maxLatencyRegressionPct = 0.2
) {
  const invalidRates: string[] = [];
  for (const [label, metrics] of [["baseline", baseline], ["canary", canary]] as const) {
    const rate = metrics.error_rate;
    if (!Number.isFinite(rate) || rate < 0 || rate > 1) invalidRates.push(`invalid_${label}_error_rate`);
  }
  if (invalidRates.length) {
    return { decision: "hold", reasons: invalidRates, error_rate_delta: null, latency_regression_pct: null };
  }
  const errorDelta = canary.error_rate - baseline.error_rate;
  const baseLatency = baseline.p95_latency_ms;
  const latencyRegression = baseLatency ? (canary.p95_latency_ms - baseLatency) / baseLatency : 0;
  const reasons: string[] = [];
  if (errorDelta > maxErrorRateDelta) reasons.push("error_rate_regression");
  if (latencyRegression > maxLatencyRegressionPct) reasons.push("latency_regression");
  return {
    decision: reasons.length ? "rollback" : "promote",
    reasons,
    error_rate_delta: Math.round(errorDelta * 10000) / 10000,
    latency_regression_pct: Math.round(latencyRegression * 10000) / 10000,
  };
}

export interface EvalCase { baseline: Metrics; canary: Metrics; expected: "promote" | "rollback" }
export const EVAL_CASES: EvalCase[] = [
  { baseline: { error_rate: 0.01, p95_latency_ms: 200 }, canary: { error_rate: 0.011, p95_latency_ms: 210 }, expected: "promote" },
  { baseline: { error_rate: 0.01, p95_latency_ms: 200 }, canary: { error_rate: 0.05, p95_latency_ms: 210 }, expected: "rollback" },
  { baseline: { error_rate: 0.01, p95_latency_ms: 200 }, canary: { error_rate: 0.011, p95_latency_ms: 500 }, expected: "rollback" },
];

export function evaluateAll() {
  const correct = EVAL_CASES.filter((c) => decide(c.baseline, c.canary).decision === c.expected).length;
  return { cases: EVAL_CASES.length, decision_accuracy: correct / EVAL_CASES.length };
}
