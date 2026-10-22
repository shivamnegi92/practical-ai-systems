import { test } from "node:test";
import { strict as assert } from "node:assert";
import { audit, cohenKappa, evaluateAll, judge, SAMPLE_ROWS } from "./app.js";

test("judge flags high lexical overlap as supported", () => {
  assert.equal(judge("The Pro plan costs $8 per month", "The Pro plan costs $8 per user per month."), "supported");
});
test("judge flags low overlap as unsupported", () => {
  assert.equal(judge("The weather is sunny today", "Notes sync automatically every 60 seconds."), "unsupported");
});
test("kappa is 1 for identical raters", () => {
  assert.equal(cohenKappa(["a", "b", "a"], ["a", "b", "a"]), 1);
});
test("audit reports agreement and kappa", () => {
  const report = audit(SAMPLE_ROWS);
  assert.equal(report.cases, SAMPLE_ROWS.length);
  assert.ok(report.judge_human_a_agreement >= 0 && report.judge_human_a_agreement <= 1);
});
test("evaluation runs end to end", () => {
  assert.equal(evaluateAll().cases, SAMPLE_ROWS.length);
});

test("numeric and polarity contradictions remain measured misses", () => {
  for (const [claim,evidence] of [["Pro costs $80 per user per month","Pro costs $8 per user per month."],["Public links can be disabled","Public links cannot be disabled."],["SMS codes are supported","SMS codes are not supported."]]) assert.equal(judge(claim,evidence), "supported");
  assert.equal(evaluateAll().cases,14);
  assert.ok(evaluateAll().judge_human_a_agreement < 1);
});
