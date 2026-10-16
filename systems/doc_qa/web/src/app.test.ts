import { BM25 } from "./app.js";
import { test } from "node:test";
import { strict as assert } from "node:assert";
import { CHUNKS, DocQA, evaluateAll } from "./app.js";

test("answers with citation", () => {
  const qa = new DocQA(CHUNKS);
  const answer = qa.answer("How much does the Pro plan cost?");
  assert.ok(answer.text.includes("$8"));
  assert.equal(answer.citations[0], "billing.md#1");
  assert.equal(answer.abstained, false);
});

test("abstains when there is no evidence", () => {
  const qa = new DocQA(CHUNKS);
  const answer = qa.answer("Does the app integrate with Salesforce CRM?");
  assert.equal(answer.abstained, true);
  assert.deepEqual(answer.citations, []);
});

test("evaluation metrics are in a reasonable range", () => {
  const metrics = evaluateAll();
  assert.ok(metrics.recall_at_3 >= 0.6);
  assert.ok(metrics.correct_abstention_rate >= 0.5);
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
