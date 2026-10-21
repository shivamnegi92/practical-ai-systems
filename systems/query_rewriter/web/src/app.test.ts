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
