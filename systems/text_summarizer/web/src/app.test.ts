import { test } from "node:test";
import { strict as assert } from "node:assert";
import { compressionRatio, evaluateAll, sentences, summarize } from "./app.js";

test("abbreviations preserve the complete example sentence", () => {
  const text = "Dr. Smith arrived at 3 p.m. today. He left. The end.";
  assert.deepEqual(sentences(text), ["Dr. Smith arrived at 3 p.m. today.", "He left.", "The end."]);
  assert.deepEqual(summarize(text, 1), ["Dr. Smith arrived at 3 p.m. today."]);
});

test("fixed abbreviation list, case and ordinary boundary controls", () => {
  for (const abbreviation of ["Dr.", "Mr.", "Mrs.", "Ms.", "e.g.", "i.e.", "a.m.", "p.m.", "etc.", "DR."]) {
    assert.deepEqual(sentences(`Use ${abbreviation} here. Next!`), [`Use ${abbreviation} here.`, "Next!"]);
  }
  assert.deepEqual(sentences("Really? Yes! Ready. Done."), ["Really?", "Yes!", "Ready.", "Done."]);
  assert.deepEqual(sentences("Notadr. Next."), ["Notadr.", "Next."]);
  assert.deepEqual(sentences(""), []);
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
