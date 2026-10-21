import { BM25 } from "./app.js";
import { expandQuery } from "./app.js";
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

test("declared pricing synonym survives the same stemming as a query", () => {
 const query="What is the PRICING?";const expanded=expandQuery(query);
 assert.ok(expanded.startsWith(query));assert.ok(expanded.split(/\s+/).includes("cost"));
 assert.equal(new BM25({billing:"cost"}).search(expanded,1)[0][0],"billing");
 assert.equal(expandQuery("unknown"),"unknown");
 assert.ok(expandQuery("unsubscribe").split(" ").includes("cancel"));
 assert.ok(expandQuery("remove").split(" ").includes("delete"));
 assert.equal(expandQuery("price").split(" ").filter(t=>t==="cost").length,1);
});
