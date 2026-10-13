// Summarize a request log into latency percentiles, cost, and budget breaches.

export interface RequestLog {
  latency_ms: number;
  cost_usd: number;
  tokens?: number;
}

export function percentile(values: number[], pct: number): number {
  const ordered = [...values].sort((a, b) => a - b);
  if (!ordered.length) return 0;
  const pos = ((ordered.length - 1) * pct) / 100;
  const lo = Math.floor(pos);
  const hi = Math.min(lo + 1, ordered.length - 1);
  return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo);
}

export function summarize(requests: RequestLog[]) {
  const latencies = requests.map((r) => r.latency_ms);
  const totalCost = requests.reduce((sum, r) => sum + r.cost_usd, 0);
  const tokens = requests.reduce((sum, r) => sum + (r.tokens ?? 0), 0);
  return {
    requests: requests.length,
    p50_latency_ms: Math.round(percentile(latencies, 50) * 100) / 100,
    p95_latency_ms: Math.round(percentile(latencies, 95) * 100) / 100,
    total_cost_usd: Math.round(totalCost * 10000) / 10000,
    cost_per_1k_tokens_usd: tokens ? Math.round(((totalCost / tokens) * 1000) * 10000) / 10000 : 0,
  };
}

export function checkBudget(summary: ReturnType<typeof summarize>, maxP95LatencyMs: number, maxCostUsd: number) {
  const reasons: string[] = [];
  if (summary.p95_latency_ms > maxP95LatencyMs) reasons.push("latency");
  if (summary.total_cost_usd > maxCostUsd) reasons.push("cost");
  return { breached: reasons.length > 0, reasons };
}

export const SAMPLE_REQUESTS: RequestLog[] = [
  { latency_ms: 120, cost_usd: 0.002, tokens: 500 },
  { latency_ms: 180, cost_usd: 0.003, tokens: 600 },
  { latency_ms: 95, cost_usd: 0.0015, tokens: 400 },
  { latency_ms: 900, cost_usd: 0.012, tokens: 2000 },
  { latency_ms: 140, cost_usd: 0.0025, tokens: 550 },
];

export interface EvalCase {
  name?: string;
  requests: RequestLog[];
  max_p95_latency_ms: number;
  max_cost_usd: number;
  gold_breached: boolean;
}
export const EVAL_CASES: EvalCase[] = [
  {
    "requests": [
      {
        "latency_ms": 100,
        "cost_usd": 0.01,
        "tokens": 1000
      },
      {
        "latency_ms": 110,
        "cost_usd": 0.01,
        "tokens": 1000
      },
      {
        "latency_ms": 120,
        "cost_usd": 0.01,
        "tokens": 1000
      },
      {
        "latency_ms": 130,
        "cost_usd": 0.01,
        "tokens": 1000
      },
      {
        "latency_ms": 500,
        "cost_usd": 0.01,
        "tokens": 1000
      }
    ],
    "max_p95_latency_ms": 300,
    "max_cost_usd": 1.0,
    "gold_breached": true
  },
  {
    "requests": [
      {
        "latency_ms": 50,
        "cost_usd": 0.001,
        "tokens": 500
      },
      {
        "latency_ms": 52,
        "cost_usd": 0.001,
        "tokens": 500
      },
      {
        "latency_ms": 55,
        "cost_usd": 0.001,
        "tokens": 500
      },
      {
        "latency_ms": 58,
        "cost_usd": 0.001,
        "tokens": 500
      },
      {
        "latency_ms": 60,
        "cost_usd": 0.001,
        "tokens": 500
      }
    ],
    "max_p95_latency_ms": 200,
    "max_cost_usd": 1.0,
    "gold_breached": false
  },
  {
    "requests": [
      {
        "latency_ms": 50,
        "cost_usd": 5.0,
        "tokens": 500
      },
      {
        "latency_ms": 52,
        "cost_usd": 5.0,
        "tokens": 500
      },
      {
        "latency_ms": 55,
        "cost_usd": 5.0,
        "tokens": 500
      },
      {
        "latency_ms": 58,
        "cost_usd": 5.0,
        "tokens": 500
      },
      {
        "latency_ms": 60,
        "cost_usd": 5.0,
        "tokens": 500
      }
    ],
    "max_p95_latency_ms": 200,
    "max_cost_usd": 1.0,
    "gold_breached": true
  },
  {
    "name": "original web demonstration",
    "requests": [
      {
        "latency_ms": 120,
        "cost_usd": 0.002,
        "tokens": 500
      },
      {
        "latency_ms": 180,
        "cost_usd": 0.003,
        "tokens": 600
      },
      {
        "latency_ms": 95,
        "cost_usd": 0.0015,
        "tokens": 400
      },
      {
        "latency_ms": 900,
        "cost_usd": 0.012,
        "tokens": 2000
      },
      {
        "latency_ms": 140,
        "cost_usd": 0.0025,
        "tokens": 550
      }
    ],
    "max_p95_latency_ms": 500,
    "max_cost_usd": 0.05,
    "gold_breached": true
  },
  {
    "name": "exact equality is within budget",
    "requests": [
      {
        "latency_ms": 100,
        "cost_usd": 0.01,
        "tokens": 100
      }
    ],
    "max_p95_latency_ms": 100,
    "max_cost_usd": 0.01,
    "gold_breached": false
  },
  {
    "name": "both thresholds exceeded",
    "requests": [
      {
        "latency_ms": 200,
        "cost_usd": 0.02,
        "tokens": 100
      }
    ],
    "max_p95_latency_ms": 100,
    "max_cost_usd": 0.01,
    "gold_breached": true
  },
  {
    "name": "empty log",
    "requests": [],
    "max_p95_latency_ms": 100,
    "max_cost_usd": 0.01,
    "gold_breached": false
  },
  {
    "name": "omitted tokens do not change verdict",
    "requests": [
      {
        "latency_ms": 100,
        "cost_usd": 0.01
      }
    ],
    "max_p95_latency_ms": 200,
    "max_cost_usd": 0.02,
    "gold_breached": false
  },
  {
    "name": "small cost crossing hidden by rounding",
    "requests": [
      {
        "latency_ms": 100,
        "cost_usd": 4e-05,
        "tokens": 100
      }
    ],
    "max_p95_latency_ms": 200,
    "max_cost_usd": 3e-05,
    "gold_breached": true
  },
  {
    "name": "small latency crossing hidden by rounding",
    "requests": [
      {
        "latency_ms": 100.004,
        "cost_usd": 0.01,
        "tokens": 100
      }
    ],
    "max_p95_latency_ms": 100.002,
    "max_cost_usd": 1,
    "gold_breached": true
  }
];

export function evaluateAll() {
  const summary = summarize(SAMPLE_REQUESTS);
  const budget = checkBudget(summary, 500, 0.05);
  const correct = EVAL_CASES.filter((c) =>
    checkBudget(summarize(c.requests), c.max_p95_latency_ms, c.max_cost_usd).breached === c.gold_breached
  ).length;
  return { summary, budget, cases: EVAL_CASES.length, breach_decision_accuracy: correct / EVAL_CASES.length };
}
