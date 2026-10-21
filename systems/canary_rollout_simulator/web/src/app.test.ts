import { test } from "node:test";

test("rejects invalid guardrail configuration while preserving zero and relaxed limits", () => {
  const base = { error_rate: .01, p95_latency_ms: 100 };
  const worse = { error_rate: .5, p95_latency_ms: 1000 };
  for (const value of [-1, NaN, Infinity, true, "0.2", null] as any[]) {
    assert.throws(() => decide(base, worse, value, .2), RangeError);
    assert.throws(() => decide(base, worse, .02, value), RangeError);
  }
  assert.equal(decide(base, base, 0, 0).decision, "promote");
  assert.equal(decide(base, { error_rate: .02, p95_latency_ms: 101 }, 0, 0).decision, "rollback");
  assert.equal(decide(base, worse, 1, 10).decision, "promote");
});
import { strict as assert } from "node:assert";
import { decide, evaluateAll } from "./app.js";

test("promotes when metrics are within thresholds", () => {
  const result = decide({ error_rate: 0.01, p95_latency_ms: 200 }, { error_rate: 0.011, p95_latency_ms: 210 });
  assert.equal(result.decision, "promote");
});
test("rolls back on error rate regression", () => {
  const result = decide({ error_rate: 0.01, p95_latency_ms: 200 }, { error_rate: 0.05, p95_latency_ms: 210 });
  assert.equal(result.decision, "rollback");
  assert.ok(result.reasons.includes("error_rate_regression"));
});
test("rolls back on latency regression", () => {
  const result = decide({ error_rate: 0.01, p95_latency_ms: 200 }, { error_rate: 0.011, p95_latency_ms: 500 });
  assert.ok(result.reasons.includes("latency_regression"));
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().decision_accuracy, 1);
});
