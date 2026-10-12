import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, SemanticCache } from "./app.js";

test("apostrophes and punctuation normalize without merging words", () => {
  const cache = new SemanticCache();
  cache.put("What's the price?", "answer");
  for (const query of ["whats the price", "What’s the price!", "whats, the price."]) {
    assert.equal(cache.get(query), "answer");
  }
  assert.equal(cache.get("whatstheprice"), null);
  assert.equal(cache.get("whats the prize"), null);
  assert.equal(cache.get("whats the price", "default", "2"), null);
  cache.put("price,USD", "amount");
  assert.equal(cache.get("price USD"), "amount");
  assert.equal(cache.get("priceUSD"), null);
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
  assert.equal(result.punctuation_hit_works, true);
  assert.equal(result.spelling_miss_works, true);
});
