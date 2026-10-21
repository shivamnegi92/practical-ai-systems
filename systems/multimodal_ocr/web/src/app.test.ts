import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, extractFields, normalizeLines } from "./app.js";

test("normalizes and sorts lines reading-order", () => {
  const lines = normalizeLines([
    { text: "  B  ", bbox: [0, 10, 10, 20] },
    { text: "A", bbox: [0, 0, 10, 10] },
  ]);
  assert.deepEqual(lines.map((l) => l.text), ["A", "B"]);
});

test("drops malformed records", () => {
  assert.deepEqual(normalizeLines([{ text: "x", bbox: [0, 0, 10] }]), []);
});

test("extracts invoice fields across lines", () => {
  const fields = extractFields([
    { text: "Invoice #", bbox: [0, 0, 60, 10] },
    { text: "INV-1001", bbox: [70, 0, 130, 10] },
    { text: "Total: $108.00", bbox: [0, 20, 100, 30] },
  ]);
  assert.equal(fields.invoice_number, "INV-1001");
  assert.equal(fields.total, "108.00");
});

test("evaluation is perfect on the bundled fixture", () => {
  assert.equal(evaluateAll().field_exact_match, 1);
});

test("normalization rejects non-finite and non-number coordinates", () => {
 for (const bad of [NaN, Infinity, -Infinity, true, false]) {
  for (let index=0; index<4; index++) {
   const box: unknown[]=[0,0,10,10]; box[index]=bad;
   assert.deepEqual(normalizeLines([{text:"bad",bbox:box}]),[]);
  }
 }
 assert.deepEqual(normalizeLines([{text:null,bbox:[0,0,1,1]}]),[]);
 assert.deepEqual(normalizeLines([{text:" ok ",bbox:[-2,-1,0,1]}]),[{text:"ok",bbox:[-2,-1,0,1]}]);
});
