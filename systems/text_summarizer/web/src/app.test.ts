import { test } from "node:test";
import { strict as assert } from "node:assert";
import { compressionRatio, evaluateAll, summarize } from "./app.js";

test("summary count is a nonnegative integer even for empty or short input", () => {
 for (const text of ["","One sentence.","First sentence. Second sentence. Third sentence."]) {
  for (const n of [-1,1.5,NaN,Infinity]) assert.throws(()=>summarize(text,n),/nonnegative integer/);
 }
 assert.throws(()=>summarize("One sentence.",JSON.parse("true")),/nonnegative integer/);
 assert.deepEqual(summarize("First sentence. Second sentence.",0),[]);
 assert.deepEqual(summarize("One sentence.",5),["One sentence."]);
});

test("short text returned unchanged", () => {
  assert.deepEqual(summarize("One sentence only."), ["One sentence only."]);
});

test("picks sentence with frequent terms", () => {
  const text =
    "Database indexing speeds up queries. Indexing indexing indexing is crucial for performance. The weather was nice yesterday.";
  const summary = summarize(text, 1);
  assert.ok(summary[0].toLowerCase().includes("indexing"));
});

test("compression ratio is a fraction of the original", () => {
  const text = "Short sentence one. Short sentence two. Short sentence three.";
  const summary = summarize(text, 1);
  const ratio = compressionRatio(text, summary);
  assert.ok(ratio > 0 && ratio < 1);
});

test("empty text has zero ratio", () => {
  assert.equal(compressionRatio("", []), 0);
});

test("evaluation recall is perfect on the bundled fixtures", () => {
  const result = evaluateAll();
  assert.equal(result.key_sentence_recall, 1);
});
