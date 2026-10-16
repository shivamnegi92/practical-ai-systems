import { test } from "node:test";
import { strict as assert } from "node:assert";
import { checkBudget, evaluateAll, percentile, summarize } from "./app.js";

test("rejects invalid measurements before summarizing or deciding a budget", () => {
  for (const field of ["latency_ms", "cost_usd", "tokens"]) {
    for (const value of [-1, NaN, Infinity, -Infinity, true, "10", null, ...(field === "tokens" ? [1.5] : [])]) {
      assert.throws(() => summarize([{ latency_ms: 10, cost_usd: .01, tokens: 100, [field]: value } as any]), RangeError);
    }
  }
  for (const field of ["p95_latency_ms", "total_cost_usd", "maxP95", "maxCost"]) {
    for (const value of [-1, NaN, Infinity, true, "10", null]) {
      const data: any = { p95_latency_ms: 10, total_cost_usd: .01, maxP95: 100, maxCost: 1, [field]: value };
      assert.throws(() => checkBudget(data, data.maxP95, data.maxCost), RangeError);
    }
  }
  assert.equal(summarize([{ latency_ms: 0, cost_usd: 0 }]).cost_per_1k_tokens_usd, 0);
  assert.equal(checkBudget(summarize([]), 0, 0).breached, false);
  assert.throws(() => summarize([{ latency_ms: 1, cost_usd: 1e308 }, { latency_ms: 1, cost_usd: 1e308 }]), RangeError);
  assert.throws(() => summarize([{ latency_ms: 1, cost_usd: 1e308, tokens: 1 }]), RangeError);
});

test("percentile of empty list is zero", () => {
  assert.equal(percentile([], 50), 0);
});
test("p50 of a simple list", () => {
  assert.equal(percentile([1, 2, 3, 4, 5], 50), 3);
});
test("summarize computes totals", () => {
  const summary = summarize([{ latency_ms: 100, cost_usd: 0.01, tokens: 1000 }]);
  assert.equal(summary.requests, 1);
  assert.equal(summary.cost_per_1k_tokens_usd, 0.01);
});
test("budget check flags latency breach", () => {
  const summary = summarize([{ latency_ms: 900, cost_usd: 0.01 }]);
  const budget = checkBudget(summary, 500, 1);
  assert.ok(budget.reasons.includes("latency"));
});
test("evaluation produces a budget verdict", () => {
  const result = evaluateAll();
  assert.ok("breached" in result.budget);
});
