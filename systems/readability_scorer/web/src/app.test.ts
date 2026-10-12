import { test } from "node:test";
import { strict as assert } from "node:assert";
import { band, evaluateAll, gradeLevel } from "./app.js";

test("short text does not have a negative grade", () => {
  assert.equal(gradeLevel("Hi"), 0);
});

test("punctuation-only text has zero grade", () => {
  assert.equal(gradeLevel("..."), 0);
});

test("short plain sentences are simple", () => {
  assert.equal(band(gradeLevel("The cat sat on the mat. It was a hot day.")), "simple");
});
test("dense long words are complex", () => {
  const text = "Notwithstanding the aforementioned stipulations, the organization's multifaceted obligations necessitate comprehensive reevaluation.";
  assert.equal(band(gradeLevel(text)), "complex");
});
test("empty text has zero grade", () => {
  assert.equal(gradeLevel(""), 0);
});
test("band boundaries", () => {
  assert.equal(band(6.0), "simple");
  assert.equal(band(6.1), "standard");
  assert.equal(band(12.1), "complex");
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().band_accuracy, 1);
});
