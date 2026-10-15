import { test } from "node:test";
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
test("evaluation exposes equal-score routing ambiguity", () => {
  assert.equal(evaluateAll().cases, 13);
  assert.equal(evaluateAll().routing_accuracy, 11/13);
});

test("equal category scores resolve while repeated single matches escalate", () => {
  for (const text of ["refund payment error crash", "password username error crash"]) assert.equal(handle({text}).status,"resolved");
  assert.equal(handle({text:"error error error"}).status,"escalated");
});
