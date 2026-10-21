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

test("run checks approval policy even when a caller supplies a false plan flag", () => {
 const calls:string[]=[];
 const agent=new BoundedAgent({write:()=>calls.push("called")},new Set(["write"]),new Set(["write"]));
 const plan={action:"write",arguments:{},requiresApproval:false};
 assert.equal(agent.run(plan).status,"awaiting_approval");assert.deepEqual(calls,[]);
 assert.equal(agent.run(plan,true).status,"completed");assert.deepEqual(calls,["called"]);
 const read=new BoundedAgent({read:()=>"ok"},new Set(["read"]),new Set(["other"]));
 assert.equal(read.run({action:"read",arguments:{},requiresApproval:true}).status,"awaiting_approval");
 assert.equal(read.run({action:"read",arguments:{},requiresApproval:false}).result,"ok");
 assert.throws(()=>read.run({action:"other",arguments:{},requiresApproval:false},true),/allow-listed/);
});
