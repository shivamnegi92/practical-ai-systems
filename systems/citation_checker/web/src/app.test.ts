import { test } from "node:test";

test("citation IDs never supply or dilute claim tokens", () => {
  for (const id of ["short", "long-document-id-with-many-words-100"]) {
    const row = checkCitations(`Orbit [${id}].`, { [id]: "Orbit" }, .8).results[0];
    assert.equal(row.status, "supported"); assert.equal(row.overlap, 1);
  }
  const falseSupport = checkCitations("Elsewhere [orbit].", { orbit: "Orbit" }).results[0];
  assert.equal(falseSupport.status, "unsupported"); assert.equal(falseSupport.overlap, 0);
  assert.equal(checkCitations("[orbit]", { orbit: "Orbit" }, 0).all_supported, false);
  assert.deepEqual(checkCitations("Orbit [alpha] [beta].", { alpha: "Orbit", beta: "Unrelated" }).results.map(r => r.overlap), [1, 0]);
});
import { strict as assert } from "node:assert";
import { checkCitations, evaluateAll, SAMPLE_CHUNKS } from "./app.js";

test("supported citation passes", () => {
  const report = checkCitations("The Pro plan costs $8 per month [billing.md#1].", SAMPLE_CHUNKS);
  assert.equal(report.all_supported, true);
});
test("documents a remaining lexical false positive without citation ID dilution", () => {
  const report = checkCitations("The Pro plan includes unlimited video calls [billing.md#1].", SAMPLE_CHUNKS);
  assert.equal(report.all_supported, true);
  assert.equal(report.results[0].overlap, 0.3333);
});
test("unknown chunk id is flagged", () => {
  const report = checkCitations("This is backed by data [made-up.md#9].", SAMPLE_CHUNKS);
  assert.equal(report.results[0].status, "unknown_chunk");
});
test("no citations means trivially all supported", () => {
  assert.equal(checkCitations("No citations here.", SAMPLE_CHUNKS).all_supported, true);
});
test("evaluation reports the remaining false positive against unchanged gold", () => {
  assert.equal(evaluateAll().accuracy, 0.75);
});
