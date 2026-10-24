import { test } from "node:test";
import { strict as assert } from "node:assert";
import { decide, evaluateAll } from "./app.js";

test("zero or missing latency baseline holds without a fabricated percentage", () => {
  for (const baseline of [{error_rate:0,p95_latency_ms:0}, {error_rate:0}]) {
    for (const duration of [0,9999]) {
      const result=decide(baseline,{error_rate:0,p95_latency_ms:duration});
      assert.equal(result.decision,"hold");
      assert.ok(result.reasons.includes("missing_latency_baseline"));
      assert.equal(result.latency_regression_pct,null);
    }
  }
});

test("known error regression still rolls back without latency baseline", () => {
  assert.equal(decide({error_rate:0,p95_latency_ms:0},{error_rate:0.05,p95_latency_ms:9999}).decision,"rollback");
});

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
