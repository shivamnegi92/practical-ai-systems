import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, route } from "./app.js";

test("billing inflections route consistently", () => {
  for (const text of ["my card was charged twice", "the card charges twice", "charging twice", "payments"]) {
    assert.equal(route(text), "billing_question");
  }
});

test("log in is a contiguous phrase including its stopword", () => {
  for (const text of ["I can't log in", "log in"]) assert.equal(route(text), "technical_issue");
  for (const text of ["log", "in log", "log outside in"]) assert.equal(route(text), "unknown");
  assert.equal(route("hello payment"), "greeting");
  assert.equal(route("greetings"), "greeting");
});

test("greeting", () => assert.equal(route("Hi there, how are you?"), "greeting"));
test("cancel request", () => assert.equal(route("I want to cancel my subscription"), "cancel_request"));
test("technical issue", () => assert.equal(route("The app keeps crashing and showing an error"), "technical_issue"));
test("unknown falls back", () => assert.equal(route("asdkj qwleoi zzxcv"), "unknown"));
test("evaluation is perfect on the bundled fixtures", () => assert.equal(evaluateAll().routing_accuracy, 1));
