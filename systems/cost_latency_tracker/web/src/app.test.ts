import { test } from "node:test";
import { strict as assert } from "node:assert";
import { checkBudget, evaluateAll, percentile, summarize } from "./app.js";

test("percentile validates its rank even for empty data", () => {
  for (const pct of [-1, 101, NaN, Infinity, -Infinity]) {
    for (const values of [[], [1, 2]]) assert.throws(() => percentile(values, pct), /percentile/);
  }
});

test("percentile preserves endpoints, interpolation and its input", () => {
  const values = [30, 10];
  assert.deepEqual([0, 25, 100].map(p => percentile(values, p)), [10, 15, 30]);
  assert.deepEqual(values, [30, 10]);
  assert.equal(percentile([], 0), 0);
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
