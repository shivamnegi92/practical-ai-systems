import { test } from "node:test";
import { strict as assert } from "node:assert";
import { checkBudget, evaluateAll, percentile, summarize } from "./app.js";

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

test("expanded budget matrix exposes rounding misses", () => {
  assert.equal(evaluateAll().cases, 10);
  assert.equal(evaluateAll().breach_decision_accuracy, 0.8);
  assert.equal(checkBudget(summarize([{latency_ms:100,cost_usd:0.00004}]),200,0.00003).breached, false);
  assert.equal(checkBudget(summarize([{latency_ms:100.004,cost_usd:0.01}]),100.002,1).breached, false);
});
