import { test } from "node:test";
import { strict as assert } from "node:assert";
import { decide, evaluateAll } from "./app.js";

test("invalid error proportions hold without computed comparison metrics", () => {
 const valid={error_rate:.01,p95_latency_ms:200};
 for (const side of ["baseline","canary"]) {
  for (const rate of [-.01,1.01,NaN,Infinity,-Infinity]) {
   const metrics={error_rate:rate,p95_latency_ms:200};
   const result=side==="baseline"?decide(metrics,valid):decide(valid,metrics);
   assert.equal(result.decision,"hold");assert.deepEqual(result.reasons,[`invalid_${side}_error_rate`]);
   assert.equal(result.error_rate_delta,null);assert.equal(result.latency_regression_pct,null);
  }
 }
 for (const bad of ["true","null",'"0.1"']) {
  const metrics=JSON.parse(`{"error_rate":${bad},"p95_latency_ms":200}`);
  assert.equal(decide(metrics,valid).decision,"hold");
 }
 assert.deepEqual(decide({...valid,error_rate:-1},{...valid,error_rate:2}).reasons,["invalid_baseline_error_rate","invalid_canary_error_rate"]);
 for (const rate of [0,1]) assert.equal(decide({...valid,error_rate:rate},{...valid,error_rate:rate}).decision,"promote");
 assert.equal(decide({...valid,error_rate:0},{...valid,error_rate:1}).decision,"rollback");
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
