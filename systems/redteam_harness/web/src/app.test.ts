import { test } from "node:test";
import { strict as assert } from "node:assert";
import { buildAgent, evaluateAll, runBattery, ATTACK_CASES } from "./app.js";

test("shared battery covers rejected invalid amounts after hardening", () => {
  const result = runBattery(buildAgent(), ATTACK_CASES);
  assert.equal(result.breach_rate, 0);
});
test("disallowed action is rejected not completed", () => {
  const result = runBattery(buildAgent(), [ATTACK_CASES[0]]);
  assert.equal(result.results[0].outcome, "rejected");
});
test("malformed arguments are rejected", () => {
  const result = runBattery(buildAgent(), [ATTACK_CASES[3]]);
  assert.equal(result.results[0].outcome, "rejected");
});
test("legit request still completes", () => {
  const result = runBattery(buildAgent(), [ATTACK_CASES[4]]);
  assert.equal(result.results[0].outcome, "completed");
});
test("evaluation reports no breaches on the hardened fixture", () => {
  assert.equal(evaluateAll().breach_rate, 0);
});

test("invalid refund gold cases are rejected without a breach", () => {
  const report=evaluateAll();
  assert.equal(report.cases,14);
  assert.deepEqual(report.results.filter(r=>r.breach).map(r=>r.name),[]);
  assert.deepEqual(report.results.filter(r=>["negative_refund_amount","string_refund_amount"].includes(r.name)).map(r=>r.outcome),["rejected","rejected"]);
});
