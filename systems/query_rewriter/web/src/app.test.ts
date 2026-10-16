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

test("declared pricing synonym survives the same stemming as a query", () => {
 const query="What is the PRICING?";const expanded=expandQuery(query);
 assert.ok(expanded.startsWith(query));assert.ok(expanded.split(/\s+/).includes("cost"));
 assert.equal(new BM25({billing:"cost"}).search(expanded,1)[0][0],"billing");
 assert.equal(expandQuery("unknown"),"unknown");
 assert.ok(expandQuery("unsubscribe").split(" ").includes("cancel"));
 assert.ok(expandQuery("remove").split(" ").includes("delete"));
 assert.equal(expandQuery("price").split(" ").filter(t=>t==="cost").length,1);
});
