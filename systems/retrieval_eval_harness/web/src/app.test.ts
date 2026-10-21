import { test } from "node:test";

test("ranking cutoffs and relevance grades must be valid before scoring", () => {
  for (const k of [-1, 1.5, NaN, Infinity, true, "2", null] as any[]) {
    assert.throws(() => recallAtK([], new Set(), k), RangeError);
    assert.throws(() => ndcgAtK([], {}, k), RangeError);
    assert.throws(() => evaluateRanking([], {}, k), RangeError);
    assert.throws(() => compareStrategies({}, [], k), RangeError);
  }
  for (const grade of [-1, NaN, Infinity, true, "1", null] as any[]) {
    assert.throws(() => ndcgAtK([], { a: grade }, 1), RangeError);
    assert.throws(() => evaluateRanking([], { a: grade }, 1), RangeError);
  }
  assert.equal(recallAtK(["a"], new Set(["a"]), 0), 0);
  assert.equal(ndcgAtK(["a"], { a: .5 }, 0), 0);
  assert.equal(ndcgAtK(["a"], { a: .5 }, 1), 1);
});
import { strict as assert } from "node:assert";
import { compareStrategies, evaluateRanking, evaluateAll, ndcgAtK, reciprocalRank, recallAtK } from "./app.js";

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
