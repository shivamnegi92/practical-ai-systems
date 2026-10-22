import { test } from "node:test";
import { strict as assert } from "node:assert";
import { CORPUS, evaluateAll, expandQuery, search } from "./app.js";

test("adds known synonym", () => {
  assert.ok(expandQuery("What is the price?").includes("cost"));
});
test("leaves unknown terms alone", () => {
  assert.equal(expandQuery("weather today"), "weather today");
});
test("baseline misses synonym-only match", () => {
  assert.deepEqual(search(CORPUS, "price information please", false), []);
});
test("expansion recovers the match", () => {
  const hits = search(CORPUS, "price information please", true);
  assert.ok(hits.length);
  assert.equal(hits[0][0], "d1");
});
test("evaluation shows expansion helps", () => {
  const result = evaluateAll();
  assert.ok(result.recall_at_1_expanded >= result.recall_at_1_baseline);
});

test("shared morphology cases expose dictionary misses without retuning", () => {
  for (const query of ["pricing information", "erasing my files"]) assert.equal(expandQuery(query),query);
  assert.ok(expandQuery("remove my files").includes("delete"));
  assert.equal(evaluateAll().cases,10);
  assert.ok(evaluateAll().recall_at_1_expanded < 1);
});
