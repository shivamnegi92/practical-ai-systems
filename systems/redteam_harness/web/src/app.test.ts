import { test } from "node:test";

test("tool failures are errors rather than successful policy rejection", () => {
  const names = new Set(["fail_type", "fail_value", "ok"]);
  const agent = new BoundedAgent({
    fail_type: () => { throw new TypeError("synthetic failure"); },
    fail_value: () => { throw new RangeError("synthetic failure"); },
    ok: () => "ok",
  }, names, names);
  const report = runBattery(agent, ["fail_type", "fail_value", "missing", "ok"].map(action => ({
    name: action, request: { action, arguments: {} }, approved: true, shouldBeAllowed: action === "ok",
  })));
  assert.deepEqual(report.results.map(r => r.outcome), ["error", "error", "rejected", "completed"]);
  assert.deepEqual(report.results.map(r => r.error_type), ["TypeError", "RangeError", undefined, undefined]);
  assert.equal(report.error_count, 2);
  assert.equal(report.cases, 4);
  assert.equal(report.breach_rate, 0);
  assert.equal(runBattery(agent, []).error_count, 0);
});
import { strict as assert } from "node:assert";
import { BoundedAgent, buildAgent, evaluateAll, runBattery, ATTACK_CASES } from "./app.js";

test("no breaches against the bundled attack battery", () => {
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
test("evaluation reports zero breaches", () => {
  assert.equal(evaluateAll().breach_rate, 0);
});
