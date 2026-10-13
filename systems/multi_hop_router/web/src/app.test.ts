import { test } from "node:test";
import { strict as assert } from "node:assert";
import { answerMultiHop, decompose, evaluateAll } from "./app.js";

test("decompose splits on 'and'", () => {
  const parts = decompose("How much does the Pro plan cost and how often do notes sync?");
  assert.equal(parts.length, 2);
});
test("answers when every sub-question is answerable", () => {
  const result = answerMultiHop("How much does the Pro plan cost and how often do notes sync?");
  assert.equal(result.abstained, false);
  assert.ok(result.citations.includes("billing.md#1"));
  assert.ok(result.citations.includes("sync.md#1"));
});
test("abstains when any sub-question is unanswerable", () => {
  const result = answerMultiHop("How much does the Pro plan cost and does it integrate with Salesforce CRM?");
  assert.equal(result.abstained, true);
});
test("handles two separately punctuated questions", () => {
  const result = answerMultiHop("How often do notes sync? How do I reset my password?");
  assert.equal(result.abstained, false);
});
test("expanded abstention matrix exposes unsupported qualifiers", () => {
  assert.equal(evaluateAll().cases, 10);
  assert.equal(evaluateAll().abstention_accuracy, 0.9);
});
