import { test } from "node:test";
import { strict as assert } from "node:assert";
import { buildAgent, evaluateAll, runBattery, ATTACK_CASES } from "./app.js";

test("shared battery measures approved invalid amount breaches", () => {
  const result = runBattery(buildAgent(), ATTACK_CASES);
  assert.equal(result.breach_rate, 2/14);
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
test("evaluation reports the two schema-policy breaches", () => {
  assert.equal(evaluateAll().breach_rate, 2/14);
});

test("only the two invalid refund gold cases count as breaches", () => {
  const report=evaluateAll();
  assert.equal(report.cases,14);
  assert.deepEqual(report.results.filter(r=>r.breach).map(r=>r.name),["negative_refund_amount","string_refund_amount"]);
});
