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

test("find duplicates returns index pairs", () => {
  const pairs = findDuplicates(["Reset my password", "Please reset my password", "Where is my order?"]);
  assert.ok(pairs.some(([i, j]) => i === 0 && j === 1));
});

test("evaluation reports semantic misses on the shared fixtures", () => {
  const result = evaluateAll();
  assert.equal(result.cases, 13);
  assert.ok(result.f1 < 1);
});

test("negation and paraphrases remain measured failures", () => {
  assert.ok(similarity("How do I enable email alerts?", "How do I not enable email alerts?") >= 0.6);
  assert.ok(similarity("How do I activate notifications?", "How do I enable alerts?") < 0.6);
});
