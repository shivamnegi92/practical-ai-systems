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

test("tools must be own callable entries as well as allow-listed", () => {
 const calls:string[]=[];
 const tools=Object.assign(Object.create({inherited:()=>calls.push("bad")}),{owned:()=>"ok"});
 const agent=new BoundedAgent(tools,new Set(["owned","inherited","constructor","toString","absent"]),new Set(["other"]));
 for (const action of ["inherited","constructor","toString","absent"]) {
  assert.throws(()=>agent.plan({action}),/allow-listed/);
  assert.throws(()=>agent.run({action,arguments:{},requiresApproval:false},true),/allow-listed/);
 }
 assert.deepEqual(calls,[]);assert.equal(agent.run(agent.plan({action:"owned"})).result,"ok");
 const broken=new BoundedAgent(JSON.parse('{"broken":0}'),new Set(["broken"]),new Set(["other"]));
 assert.throws(()=>broken.plan({action:"broken"}),/allow-listed/);
 assert.throws(()=>broken.run({action:"broken",arguments:{},requiresApproval:false},true),/allow-listed/);
});
