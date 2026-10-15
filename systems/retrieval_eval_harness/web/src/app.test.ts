import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, ndcgAtK, reciprocalRank, recallAtK, compareStrategies, CORPUS, QUERIES } from "./app.js";

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

test("shared judgments expose missing second targets and synonym misses", () => {
  assert.equal(QUERIES.length,11);
  const both=compareStrategies(CORPUS,[{text:"business day",relevance:{d3:1,d4:1}}]);
  assert.equal(both.expanded.recall_at_k,0.5);
  for (const [text,gold] of [["membership tariff","d1"],["end subscription","d3"]]) assert.equal(compareStrategies(CORPUS,[{text,relevance:{[gold]:1}}]).expanded.recall_at_k,0);
});
