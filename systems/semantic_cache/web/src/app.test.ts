import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, SemanticCache } from "./app.js";

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

test("capacity must be a positive integer", () => {
  for (const value of [0,-1,1.5,NaN,Infinity,-Infinity]) assert.throws(()=>new SemanticCache(value));
});
test("ttl must be finite and positive", () => {
  for (const value of [0,-1,NaN,Infinity,-Infinity]) assert.throws(()=>new SemanticCache(1,value));
});
test("fractional positive ttl expires at its exact boundary", () => {
  let time=0;
  const cache=new SemanticCache(1,0.5,()=>time);
  cache.put("a","x"); assert.equal(cache.get("a"),"x");
  time=0.5; assert.equal(cache.get("a"),null);
});
