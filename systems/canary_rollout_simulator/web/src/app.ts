// Two-sample canary guardrail check for a promote/rollback/hold decision.
// A fixed-threshold comparison, not a statistically rigorous A/B test: it
// ignores sample size, variance, and confidence intervals.

export interface Metrics {
  error_rate: number;
  p95_latency_ms: number;
}

export function decide(
  baseline: Pick<Metrics, "error_rate"> & Partial<Pick<Metrics, "p95_latency_ms">>,
  canary: Metrics,
  maxErrorRateDelta = 0.02,
  maxLatencyRegressionPct = 0.2
) {
  const errorDelta = canary.error_rate - baseline.error_rate;
  const baseLatency = baseline.p95_latency_ms;
  const latencyRegression = baseLatency !== undefined && baseLatency > 0 ? (canary.p95_latency_ms - baseLatency) / baseLatency : null;
  const reasons: string[] = [];
  if (errorDelta > maxErrorRateDelta) reasons.push("error_rate_regression");
  if (latencyRegression !== null && latencyRegression > maxLatencyRegressionPct) reasons.push("latency_regression");
  const decision = reasons.length ? "rollback" : latencyRegression === null ? "hold" : "promote";
  if (latencyRegression === null) reasons.push("missing_latency_baseline");
  return {
    decision,
    reasons,
    error_rate_delta: Math.round(errorDelta * 10000) / 10000,
    latency_regression_pct: latencyRegression !== null ? Math.round(latencyRegression * 10000) / 10000 : null,
  };
}

export interface EvalCase { baseline: Pick<Metrics, "error_rate"> & Partial<Pick<Metrics, "p95_latency_ms">>; canary: Metrics; expected: "promote" | "rollback" | "hold" }
export const EVAL_CASES: EvalCase[] = [
  { baseline: {error_rate:0,p95_latency_ms:0}, canary: {error_rate:0,p95_latency_ms:9999}, expected: "hold" },
  { baseline: {error_rate:0}, canary: {error_rate:0,p95_latency_ms:9999}, expected: "hold" },
  { baseline: {error_rate:0,p95_latency_ms:0}, canary: {error_rate:0,p95_latency_ms:0}, expected: "hold" },
  { baseline: {error_rate:0,p95_latency_ms:0}, canary: {error_rate:0.05,p95_latency_ms:9999}, expected: "rollback" },
  { baseline: { error_rate: 0.01, p95_latency_ms: 200 }, canary: { error_rate: 0.011, p95_latency_ms: 210 }, expected: "promote" },
  { baseline: { error_rate: 0.01, p95_latency_ms: 200 }, canary: { error_rate: 0.05, p95_latency_ms: 210 }, expected: "rollback" },
  { baseline: { error_rate: 0.01, p95_latency_ms: 200 }, canary: { error_rate: 0.011, p95_latency_ms: 500 }, expected: "rollback" },
];

export function evaluateAll() {
  const correct = EVAL_CASES.filter((c) => decide(c.baseline, c.canary).decision === c.expected).length;
  return { cases: EVAL_CASES.length, decision_accuracy: correct / EVAL_CASES.length };
}
