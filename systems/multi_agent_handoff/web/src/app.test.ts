import { test } from "node:test";

test("tied triage escalates without choosing a specialist", () => {
  for (const [text, score] of [["invoice payment error login", 2], ["invoice payment error login username profile", 2], ["invoice error", 1], ["hello", 0]] as const) {
    assert.deepEqual(handle({ text }), { status: "escalated", category: null, confidence: score });
  }
  assert.equal(handle({ text: "invoice payment refund error login" }).category, "billing");
  assert.equal(handle({ text: "invoice payment error login crash" }).category, "technical");
});
import { strict as assert } from "node:assert";
import { evaluateAll, handle, triage } from "./app.js";

test("routes a clear billing request", () => {
  const result = handle({ text: "I was charged for my invoice payment" });
  assert.equal(result.status, "resolved");
  assert.equal(result.category, "billing");
});
test("escalates a low-confidence request", () => {
  const result = handle({ text: "Hello there" });
  assert.equal(result.status, "escalated");
});
test("triage returns null category with no keyword matches", () => {
  const [category, confidence] = triage("Hello there");
  assert.equal(category, null);
  assert.equal(confidence, 0);
});
test("single keyword match still escalates below threshold", () => {
  const result = handle({ text: "There's a bug somewhere" });
  assert.equal(result.status, "escalated");
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().routing_accuracy, 1);
});
