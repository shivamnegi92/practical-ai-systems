import { test } from "node:test";
import { strict as assert } from "node:assert";
import { detectDrift, evaluateAll, type Schema } from "./app.js";

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

test("the expanded shared matrix includes known container limitations", () => {
  assert.equal(evaluateAll().cases,10);
  assert.equal(evaluateAll().exact_report_match,0.8);
});
