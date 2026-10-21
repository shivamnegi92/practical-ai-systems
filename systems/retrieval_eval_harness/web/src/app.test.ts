import { BM25 } from "./app.js";
import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, ndcgAtK, reciprocalRank, recallAtK } from "./app.js";

test("recall@k over relevant set", () => {
  assert.equal(recallAtK(["a", "b", "c"], new Set(["b"]), 2), 1);
});
test("reciprocal rank finds first relevant hit", () => {
  assert.equal(reciprocalRank(["a", "b", "c"], new Set(["b"])), 0.5);
});
test("ndcg is 1 for perfectly ranked relevance", () => {
  assert.equal(ndcgAtK(["a", "b"], { a: 1, b: 0 }, 2), 1);
});
test("evaluation shows expansion helps or matches baseline", () => {
  const result = evaluateAll();
  assert.ok(result.expanded.recall_at_k >= result.baseline.recall_at_k);
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
