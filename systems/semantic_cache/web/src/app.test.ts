import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, SemanticCache } from "./app.js";

test("expired MRU is discarded before a live LRU entry", () => {
 let now=0;const c=new SemanticCache(2,5,()=>now);
 c.put("expired","old");now=4;c.put("live","keep");c.get("expired");
 now=5;c.put("new","new");
 assert.equal(c.stats().hits,1);assert.equal(c.stats().misses,0);
 assert.equal(c.get("live"),"keep");assert.equal(c.get("new"),"new");assert.equal(c.get("expired"),null);
});

test("replacing an expired entry starts a fresh TTL", () => {
 let now=0;const c=new SemanticCache(1,5,()=>now);
 c.put("a","old");now=5;c.put("a","replacement");assert.equal(c.get("a"),"replacement");
 now=10;assert.equal(c.get("a"),null);
});

test("normalized queries hit the same entry", () => {
  const cache = new SemanticCache();
  cache.put("What is the price?", "answer");
  assert.equal(cache.get("what   is the PRICE?"), "answer");
});

test("misses increment the miss counter", () => {
  const cache = new SemanticCache();
  cache.get("nothing cached");
  assert.equal(cache.stats().misses, 1);
});

test("entries expire after ttl", () => {
  let time = 0;
  const cache = new SemanticCache(10, 100, () => time);
  cache.put("q", "a");
  time = 200;
  assert.equal(cache.get("q"), null);
});

test("evicts least recently used entry over capacity", () => {
  const cache = new SemanticCache(1);
  cache.put("a", "1");
  cache.put("b", "2");
  assert.equal(cache.get("a"), null);
  assert.equal(cache.get("b"), "2");
});

test("evaluation demonstrates both eviction and expiry", () => {
  const result = evaluateAll();
  assert.equal(result.lru_eviction_works, true);
  assert.equal(result.ttl_expiry_works, true);
});
