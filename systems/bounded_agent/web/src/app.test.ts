import { BoundedAgent } from "./app.js";
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

test("approval defaults differ from an explicit empty set", () => {
 const tools={read:()=>"ok",write:()=>"done"};const allowed=new Set(Object.keys(tools));
 for (const agent of [new BoundedAgent(tools,allowed),new BoundedAgent(tools,allowed,undefined)]) {
  const plan=agent.plan({action:"read"}); assert.equal(plan.requiresApproval,true);
  assert.equal(agent.run(plan).status,"awaiting_approval");
 }
 for (const required of [new Set<string>(),new Set(["write"])]) {
  const agent=new BoundedAgent(tools,allowed,required);
  assert.equal(agent.run(agent.plan({action:"read"})).result,"ok");
  assert.equal(agent.plan({action:"write"}).requiresApproval,required.has("write"));
  assert.throws(()=>agent.plan({action:"unknown"}),/allow-listed/);
 }
});
