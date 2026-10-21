import { test } from "node:test";
import { strict as assert } from "node:assert";
import { detectDrift, evaluateAll, type Schema } from "./app.js";

test("JSON container names and list/dict aliases stay distinct", () => {
 for (const [kind,values] of [["array",[[],[1]]],["list",[[],[1]]],["object",[{}, {x:1}]],["dict",[{}, {x:1}]]] as Array<[string,unknown[]]>) {
  for (const value of values) assert.equal(detectDrift({value:{type:kind,required:true}},[{value}]).drift_detected,false);
 }
 for (const [kind,value] of [["array",{}],["list",{}],["object",[]],["dict",[]]] as Array<[string,unknown]>) {
  assert.deepEqual(detectDrift({value:{type:kind}},[{value}]).type_mismatched_fields,["value"]);
 }
 const result=detectDrift({value:{type:"array",required:true}},[{value:null}]);
 assert.deepEqual(result.missing_required_fields,["value"]);assert.deepEqual(result.type_mismatched_fields,[]);
});

const SCHEMA: Schema = { id: { type: "number", required: true }, name: { type: "string", required: true } };

test("detects a new field", () => {
  const result = detectDrift(SCHEMA, [{ id: 1, name: "A", extra: "x" }]);
  assert.deepEqual(result.new_fields, ["extra"]);
});
test("detects a missing required field", () => {
  const result = detectDrift(SCHEMA, [{ id: 1 }]);
  assert.deepEqual(result.missing_required_fields, ["name"]);
});
test("detects a type mismatch", () => {
  const result = detectDrift(SCHEMA, [{ id: "one", name: "A" }]);
  assert.deepEqual(result.type_mismatched_fields, ["id"]);
});
test("no drift on clean records", () => {
  const result = detectDrift(SCHEMA, [{ id: 1, name: "A" }]);
  assert.equal(result.drift_detected, false);
});
test("evaluation flags drift on the bundled fixture", () => {
  assert.equal(evaluateAll().matches_expected_drift, true);
});
