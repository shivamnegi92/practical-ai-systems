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

export interface EvalCase { name?: string | null; baseline: Metrics; canary: Metrics; expected: "promote" | "rollback" | "hold" }
export const EVAL_CASES: EvalCase[] = [
  {
    "name": null,
    "baseline": {
      "error_rate": 0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.015,
      "p95_latency_ms": 210
    },
    "expected": "promote"
  },
  {
    "name": null,
    "baseline": {
      "error_rate": 0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.05,
      "p95_latency_ms": 205
    },
    "expected": "rollback"
  },
  {
    "name": null,
    "baseline": {
      "error_rate": 0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.012,
      "p95_latency_ms": 400
    },
    "expected": "rollback"
  },
  {
    "name": "original web promote",
    "baseline": {
      "error_rate": 0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.011,
      "p95_latency_ms": 210
    },
    "expected": "promote"
  },
  {
    "name": "original web error regression",
    "baseline": {
      "error_rate": 0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.05,
      "p95_latency_ms": 210
    },
    "expected": "rollback"
  },
  {
    "name": "original web latency regression",
    "baseline": {
      "error_rate": 0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.011,
      "p95_latency_ms": 500
    },
    "expected": "rollback"
  },
  {
    "name": "exact error threshold",
    "baseline": {
      "error_rate": 0,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.02,
      "p95_latency_ms": 200
    },
    "expected": "promote"
  },
  {
    "name": "exact latency threshold",
    "baseline": {
      "error_rate": 0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.01,
      "p95_latency_ms": 240
    },
    "expected": "promote"
  },
  {
    "name": "both regressions",
    "baseline": {
      "error_rate": 0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.05,
      "p95_latency_ms": 400
    },
    "expected": "rollback"
  },
  {
    "name": "improved metrics",
    "baseline": {
      "error_rate": 0.02,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0.01,
      "p95_latency_ms": 150
    },
    "expected": "promote"
  },
  {
    "name": "invalid negative baseline rate",
    "baseline": {
      "error_rate": -0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 0,
      "p95_latency_ms": 200
    },
    "expected": "hold"
  },
  {
    "name": "invalid canary rate above one",
    "baseline": {
      "error_rate": 0.01,
      "p95_latency_ms": 200
    },
    "canary": {
      "error_rate": 1.1,
      "p95_latency_ms": 200
    },
    "expected": "hold"
  }
];

export function evaluateAll() {
  const correct = EVAL_CASES.filter((c) => decide(c.baseline, c.canary).decision === c.expected).length;
  return { cases: EVAL_CASES.length, decision_accuracy: correct / EVAL_CASES.length };
}
