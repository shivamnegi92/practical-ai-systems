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
