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

test("BM25 result count is a nonnegative integer even for an empty index", () => {
 for (const docs of [{},{a:"term",b:"term"}] as Record<string,string>[]) {
  const index=new BM25(docs);
  for (const k of [-1,1.5,NaN,Infinity]) assert.throws(()=>index.search("term",k),/nonnegative integer/);
  assert.throws(()=>index.search("term",JSON.parse("true")),/nonnegative integer/);
  assert.deepEqual(index.search("term",0),[]);
  assert.equal(index.search("term",5).length,Object.keys(docs).length);
  assert.equal(index.search("term",1).length,Math.min(1,Object.keys(docs).length));
 }
});
