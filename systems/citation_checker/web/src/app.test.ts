import { test } from "node:test";
import { strict as assert } from "node:assert";
import { checkCitations, evaluateAll, SAMPLE_CHUNKS } from "./app.js";

test("changed numeric facts are unsupported with number_mismatch", () => {
  const pairs = [
    ["The Pro plan costs $80 per user per month.","The Pro plan costs $8 per user per month."],
    ["The deadline is 2026-01-02.","The deadline is 2026-01-01."],
    ["The discount rate is 20%.","The discount rate is 2%."],
    ["The quota allows 80 requests.","The quota allows 8 requests."],
    ["The average duration is 1.50 seconds.","The average duration is 1.05 seconds."],
    ["The Pro plan costs €8 per user per month.","The Pro plan costs $8 per user per month."],
  ];
  for (const [claim,source] of pairs) {
    const row=checkCitations(claim.slice(0,-1)+" [ref#99].",{"ref#99":source}).results[0];
    assert.equal(row.status,"unsupported");
    assert.equal(row.reason,"number_mismatch");
  }
});

test("matching values ignore numeric citation IDs", () => {
  const claim="The Pro plan costs $8 and renews on 2026-01-01 with a 2% discount";
  assert.equal(checkCitations(claim+" [ref#99].",{"ref#99":claim+"."}).all_supported,true);
});

test("supported citation passes", () => {
  const report = checkCitations("The Pro plan costs $8 per month [billing.md#1].", SAMPLE_CHUNKS);
  assert.equal(report.all_supported, true);
});
test("unsupported claim is flagged", () => {
  const report = checkCitations("The Pro plan includes unlimited video calls [billing.md#1].", SAMPLE_CHUNKS);
  assert.equal(report.all_supported, false);
});
test("unknown chunk id is flagged", () => {
  const report = checkCitations("This is backed by data [made-up.md#9].", SAMPLE_CHUNKS);
  assert.equal(report.results[0].status, "unknown_chunk");
});
test("no citations means trivially all supported", () => {
  assert.equal(checkCitations("No citations here.", SAMPLE_CHUNKS).all_supported, true);
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().accuracy, 1);
});
