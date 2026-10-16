import { test } from "node:test";

test("trace inputs reject invalid durations and thresholds before scoring", () => {
 for (const value of [-1,NaN,Infinity,-Infinity]) {
  assert.throws(()=>detectAnomalies([10,value],[]),/baseline/);
  assert.throws(()=>detectAnomalies([10,20],[{name:"bad",duration_ms:value}]),/duration/);
  assert.throws(()=>detectAnomalies([],[],value),/threshold/);
 }
 for (const value of [true,null,"1"]) {
  const bad=JSON.parse(JSON.stringify(value));
  assert.throws(()=>detectAnomalies([10,bad],[]),/baseline/);
  assert.throws(()=>detectAnomalies([10,20],[{name:"bad",duration_ms:bad}]),/duration/);
  assert.throws(()=>detectAnomalies([],[],bad),/threshold/);
 }
 const result=detectAnomalies([10,20],[{name:"normal",duration_ms:15},{name:"flagged",duration_ms:15,error:true}],.5);
 assert.equal(result[0].anomalous,false);assert.equal(result[1].anomalous,true);
 assert.deepEqual(detectAnomalies([],[],0),[]);
});
import { strict as assert } from "node:assert";
import { BASELINE, detectAnomalies, evaluateAll, TRACES } from "./app.js";

test("normal durations are not anomalous", () => {
  const results = detectAnomalies(BASELINE, [{ name: "n", duration_ms: 101 }]);
  assert.equal(results[0].anomalous, false);
});
test("far outlier duration is anomalous", () => {
  const results = detectAnomalies(BASELINE, [{ name: "n", duration_ms: 400 }]);
  assert.equal(results[0].anomalous, true);
});
test("explicit error flag is always anomalous", () => {
  const results = detectAnomalies(BASELINE, [{ name: "n", duration_ms: 100, error: true }]);
  assert.equal(results[0].anomalous, true);
});
test("detects all four bundled traces correctly", () => {
  const results = detectAnomalies(BASELINE, TRACES);
  assert.deepEqual(results.map((r) => r.anomalous), [false, false, true, true]);
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().f1, 1);
});
