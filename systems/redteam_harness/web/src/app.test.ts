import { BoundedAgent } from "./app.js";
import { test } from "node:test";
import { strict as assert } from "node:assert";
import { buildAgent, evaluateAll, runBattery, ATTACK_CASES } from "./app.js";

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

test("null requests and array plans are rejected before tool invocation", () => {
  let calls = 0;
  const agent = new BoundedAgent({ echo: () => { calls++; return "ok"; } }, new Set(["echo"]), new Set(["echo"]));
  assert.throws(() => agent.plan({ action: "echo", arguments: null }), /arguments must be an object/);
  assert.throws(() => agent.run({ action: "echo", arguments: [] as any, requiresApproval: true }, true), /arguments must be an object/);
  assert.equal(calls, 0);
  assert.equal(agent.run(agent.plan({ action: "echo" }), true).status, "completed");
  assert.equal(agent.run(agent.plan({ action: "echo", arguments: {} }), true).status, "completed");
  assert.equal(calls, 2);
});
