import { test } from "node:test";
import { strict as assert } from "node:assert";
import { buildSampleAgent, evaluateAll } from "./app.js";

test("allow-listed action without approval requirement completes", () => {
  const agent = buildSampleAgent();
  const plan = agent.plan({ action: "lookup_order", arguments: { order_id: "A1" } });
  assert.equal(agent.run(plan).status, "completed");
});
test("sensitive action awaits approval", () => {
  const agent = buildSampleAgent();
  const plan = agent.plan({ action: "send_refund", arguments: { amount: 10 } });
  assert.equal(agent.run(plan, false).status, "awaiting_approval");
});
test("approved sensitive action completes", () => {
  const agent = buildSampleAgent();
  const plan = agent.plan({ action: "send_refund", arguments: { amount: 10 } });
  assert.equal(agent.run(plan, true).status, "completed");
});
test("disallowed action is rejected at plan time", () => {
  const agent = buildSampleAgent();
  assert.throws(() => agent.plan({ action: "delete_account", arguments: {} }));
});
test("evaluation demonstrates the full policy", () => {
  const result = evaluateAll();
  assert.ok(Object.values(result).every(Boolean));
});

test("expanded matrix counts refusal and approval controls", () => {
  const result = evaluateAll();
  assert.equal(result.cases, 10);
  assert.equal(result.policy_cases_passed, 10);
  assert.equal(result.policy_accuracy, 1);
});
