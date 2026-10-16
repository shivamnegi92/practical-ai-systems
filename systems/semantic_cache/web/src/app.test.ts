import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, SemanticCache } from "./app.js";

test("embedded delimiters cannot alias cache namespace fields", () => {
 const triples:[string,string,string][]=[["q","a","b\0c"],["q","a\0b","c"],["c\0q","a","b"]];
 const c=new SemanticCache();assert.equal(new Set(triples.map(t=>SemanticCache.key(...t))).size,3);
 triples.forEach(([q,m,v],i)=>c.put(q,String(i),m,v));
 triples.forEach(([q,m,v],i)=>assert.equal(c.get(q,m,v),String(i)));
 c.put(" Hello  WORLD ","ok",'model"\\name',"version\n1");
 assert.equal(c.get("hello world",'model"\\name',"version\n1"),"ok");
 assert.equal(c.get("hello world",'model"\\name',"other"),null);
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
