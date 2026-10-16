import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, ndcgAtK, reciprocalRank, recallAtK } from "./app.js";

test("ndcg credits each judged document once without closing duplicate rank slots", () => {
 assert.equal(ndcgAtK(["a","a"],{a:1},2),1);
 for (const k of [2,3]) assert.equal(ndcgAtK(["a","a","b"],{a:2,b:1},k),ndcgAtK(["a","missing","b"],{a:2,b:1},k));
 assert.equal(ndcgAtK(["a","b"],{a:2,b:1},2),1);
 assert.equal(ndcgAtK(["missing","missing"],{a:1},2),0);
 assert.equal(ndcgAtK(["a","a"],{a:0},2),0);
 assert.equal(ndcgAtK(["constructor","a"],{a:1},2),1/Math.log2(3));
});

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
