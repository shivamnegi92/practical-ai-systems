import { test } from "node:test";
import { strict as assert } from "node:assert";
import { BASELINE, detectAnomalies, evaluateAll, TRACES } from "./app.js";

test("flat baseline applies a strict 50 percent deviation tolerance", () => {
  const traces = [10000,100,150,151,50,49].map((duration_ms) => ({name:String(duration_ms),duration_ms}));
  assert.deepEqual(detectAnomalies([100,100,100],traces).map((r)=>r.anomalous), [true,false,false,true,false,true]);
});

test("zero mean is distinct from missing history", () => {
  const traces = [0,1].map((duration_ms)=>({name:String(duration_ms),duration_ms}));
  assert.deepEqual(detectAnomalies([0,0],traces).map((r)=>r.anomalous), [false,true]);
  assert.deepEqual(detectAnomalies([],traces).map((r)=>r.anomalous), [false,false]);
  assert.equal(detectAnomalies([], [{name:"error",duration_ms:0,error:true}])[0].anomalous,true);
});

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
