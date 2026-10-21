import { test } from "node:test";
import { strict as assert } from "node:assert";
import { checkCaption, evaluateAll } from "./app.js";

test("phrase matching normalizes whitespace and respects word boundaries", () => {
  for (const phrase of ["IMAGE   OF", "picture\tof", "no caption\navailable", "untitled  image"]) {
    assert.ok(checkCaption(phrase + " a dog running").reasons.some(r => r.startsWith("banned_phrase:")));
  }
  assert.equal(checkCaption("A scarf hangs outside.", ["car"]).passed, false);
  assert.equal(checkCaption("A red carpet outside.", ["red car"]).passed, false);
  assert.equal(checkCaption("A RED\tCAR waits outside.", ["red  car"]).passed, true);
  assert.equal(checkCaption("A (car) waits outside.", ["car"]).passed, true);
  assert.equal(checkCaption("A C++ manual lies open.", ["C++"]).passed, true);
  assert.equal(checkCaption("A dog runs outside.", ["  "]).passed, false);
  assert.equal(checkCaption("A sculpture with a miniatureimage of clouds.").passed, true);
});

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
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().accuracy, 1);
});
