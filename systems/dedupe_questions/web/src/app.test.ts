import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, findDuplicates, similarity } from "./app.js";

test("identical meaning is high similarity", () => {
  assert.ok(similarity("How do I reset my password?", "How can I reset my password?") >= 0.6);
});

test("unrelated questions are low similarity", () => {
  assert.ok(similarity("What is your refund policy?", "Where is my order?") < 0.3);
});

test("empty strings are identical", () => {
  assert.equal(similarity("", ""), 1);
});

test("different stopword-only questions are not duplicates", () => {
  assert.equal(similarity("Who are you?", "What is it?"), 0);
  assert.equal(similarity("What is it?", "what is it"), 1);
  assert.deepEqual(findDuplicates(["Who are you?", "What is it?"]), []);
});
test("find duplicates returns index pairs", () => {
  const pairs = findDuplicates(["Reset my password", "Please reset my password", "Where is my order?"]);
  assert.ok(pairs.some(([i, j]) => i === 0 && j === 1));
});

test("evaluation is perfect on the bundled fixtures", () => {
  const result = evaluateAll();
  assert.equal(result.f1, 1);
});
