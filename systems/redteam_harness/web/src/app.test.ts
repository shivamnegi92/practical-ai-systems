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
