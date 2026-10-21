import { test } from "node:test";

test("duplicate threshold must be a valid proportion even with no pairs", () => {
 for (const questions of [[],["same question","same question"]]) {
  for (const value of [-.1,1.1,NaN,Infinity]) {
   assert.throws(()=>findDuplicates(questions,value),/threshold/);
   assert.throws(()=>evaluateAll(value),/threshold/);
  }
  for (const value of [true,null,"0.5"]) assert.throws(()=>findDuplicates(questions,JSON.parse(JSON.stringify(value))),/threshold/);
 }
 assert.deepEqual(findDuplicates(["same question","same question"],1),[[0,1,1]]);
 assert.equal(findDuplicates(["cats","dogs"],0).length,1);
});
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

test("evaluation is perfect on the bundled fixtures", () => {
  const result = evaluateAll();
  assert.equal(result.f1, 1);
});
