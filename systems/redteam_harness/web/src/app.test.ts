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
