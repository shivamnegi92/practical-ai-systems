import { test } from "node:test";
import { strict as assert } from "node:assert";
import { classify, evaluateAll } from "./app.js";

test("negation flips each polarity, including contractions", () => {
  for (const text of ["This is not good", "never good", "no good", "isn't good"]) {
    assert.equal(classify(text), "negative");
  }
  for (const text of ["not bad at all", "isn’t bad"]) assert.equal(classify(text), "positive");
});

test("negation window is three previous tokens", () => {
  assert.equal(classify("not at all good"), "negative");
  assert.equal(classify("not really at all good"), "positive");
});

test("other apostrophes preserve existing word matches", () => {
  assert.equal(classify("good's meaning"), "positive");
});

test("positive words win", () => {
  assert.equal(classify("This product is great and the support team is fantastic."), "positive");
});
test("negative words win", () => {
  assert.equal(classify("The checkout process is slow and confusing."), "negative");
});
test("no lexicon words is neutral", () => {
  assert.equal(classify("It's okay, does the job."), "neutral");
});
test("tied counts default to neutral", () => {
  assert.equal(classify("I love this app but the login page is terrible."), "neutral");
});
test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().accuracy, 1);
});
