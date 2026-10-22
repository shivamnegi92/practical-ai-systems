import { test } from "node:test";
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
test("evaluation preserves two invalid-rate failures", () => {
  assert.equal(evaluateAll().cases, 12);
  assert.equal(evaluateAll().decision_accuracy, 10 / 12);
});
