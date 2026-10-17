import { BM25 } from "./app.js";
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

test("BM25 treats reserved object names as document IDs", () => {
  const docs = Object.fromEntries(["__proto__", "constructor", "toString", "normal"].map(id => [id, "orbit"]));
  const index = new BM25(docs);
  assert.deepEqual(Object.keys(index.tokens).sort(), Object.keys(docs).sort());
  const hits = index.search("orbit", 10);
  assert.deepEqual(hits.map(([id]) => id).sort(), Object.keys(docs).sort());
  assert.ok(hits.every(([, score]) => Number.isFinite(score) && score > 0));
  assert.equal(new Set(hits.map(([, score]) => score)).size, 1);
});
