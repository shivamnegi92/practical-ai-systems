import { test } from "node:test";
import { strict as assert } from "node:assert";
import { checkCaption, evaluateAll, EVAL_CASES } from "./app.js";

test("good caption passes", () => {
  assert.equal(checkCaption("A golden retriever running across a sunny beach.").passed, true);
});
test("placeholder caption is banned", () => {
  const result = checkCaption("image of a dog");
  assert.equal(result.passed, false);
  assert.ok(result.reasons.some((r) => r.startsWith("banned_phrase")));
});
test("too short caption fails", () => {
  assert.ok(checkCaption("A cat.").reasons.includes("too_short"));
});
test("missing required keyword fails", () => {
  const result = checkCaption("A red sports car.", ["truck"]);
  assert.ok(result.reasons.some((r) => r.startsWith("missing_keywords")));
});
test("evaluation reports whitespace and substring misses honestly", () => {
  assert.equal(evaluateAll().cases, 16);
  assert.equal(evaluateAll().accuracy, 0.75);
});

test("shared gold matrix keeps the four intended failures", () => {
  const missed = EVAL_CASES.filter(c => checkCaption(c.caption, c.required).passed !== c.passed).map(c => c.caption);
  assert.deepEqual(missed, ["image   of a dog", "picture\tof a dog", "A carpet covers the floor.", "A cart rests near the wall."]);
});
