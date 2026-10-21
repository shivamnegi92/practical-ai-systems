// Summarize a request log into latency percentiles, cost, and budget breaches.

export interface RequestLog {
  latency_ms: number;
  cost_usd: number;
  tokens?: number;
}

function measurement(value: number, name: string, integer = false): void {
  if (typeof value !== "number" || !Number.isFinite(value) || value < 0 || (integer && !Number.isInteger(value))) {
    throw new RangeError(`${name} must be a finite nonnegative ${integer ? "integer" : "number"}`);
  }
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
  requests.forEach((request, i) => {
    measurement(request.latency_ms, `requests[${i}].latency_ms`);
    measurement(request.cost_usd, `requests[${i}].cost_usd`);
    measurement(request.tokens === undefined ? 0 : request.tokens, `requests[${i}].tokens`, true);
  });
  const latencies = requests.map((r) => r.latency_ms);
  const totalCost = requests.reduce((sum, r) => sum + r.cost_usd, 0);
  const tokens = requests.reduce((sum, r) => sum + (r.tokens ?? 0), 0);
  const summary = {
    requests: requests.length,
    p50_latency_ms: Math.round(percentile(latencies, 50) * 100) / 100,
    p95_latency_ms: Math.round(percentile(latencies, 95) * 100) / 100,
    total_cost_usd: Math.round(totalCost * 10000) / 10000,
    cost_per_1k_tokens_usd: tokens ? Math.round(((totalCost / tokens) * 1000) * 10000) / 10000 : 0,
  };
  for (const [field, value] of Object.entries(summary)) measurement(value, field);
  return summary;
}

export function checkBudget(summary: ReturnType<typeof summarize>, maxP95LatencyMs: number, maxCostUsd: number) {
  measurement(summary.p95_latency_ms, "p95_latency_ms");
  measurement(summary.total_cost_usd, "total_cost_usd");
  measurement(maxP95LatencyMs, "maxP95LatencyMs");
  measurement(maxCostUsd, "maxCostUsd");
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

export function evaluateAll() {
  const summary = summarize(SAMPLE_REQUESTS);
  const budget = checkBudget(summary, 500, 0.05);
  return { summary, budget };
}
