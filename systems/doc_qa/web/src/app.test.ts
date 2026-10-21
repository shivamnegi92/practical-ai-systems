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

test("BM25 treats reserved object names as document IDs", () => {
  const docs = Object.fromEntries(["__proto__", "constructor", "toString", "normal"].map(id => [id, "orbit"]));
  const index = new BM25(docs);
  assert.deepEqual(Object.keys(index.tokens).sort(), Object.keys(docs).sort());
  const hits = index.search("orbit", 10);
  assert.deepEqual(hits.map(([id]) => id).sort(), Object.keys(docs).sort());
  assert.ok(hits.every(([, score]) => Number.isFinite(score) && score > 0));
  assert.equal(new Set(hits.map(([, score]) => score)).size, 1);
});
