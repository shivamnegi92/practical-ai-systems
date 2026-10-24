import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, scoreTurns, SAMPLE_TURNS, EVAL_CALLS } from "./app.js";

test("task success when the required action is mentioned", () => {
  const result = scoreTurns(SAMPLE_TURNS, ["cancel subscription"]);
  assert.equal(result.task_success, true);
});
test("flags a missing requirement", () => {
  const result = scoreTurns(SAMPLE_TURNS, ["process a refund"]);
  assert.equal(result.task_success, false);
  assert.ok(result.missing_requirements.includes("process a refund"));
});
test("flags a forbidden action violation", () => {
  const result = scoreTurns(SAMPLE_TURNS, [], ["cancel_subscription"]);
  assert.equal(result.safe, false);
});
test("computes median latency across agent turns", () => {
  const result = scoreTurns(SAMPLE_TURNS, []);
  assert.equal(result.median_latency_ms, 650);
});
test("evaluation matches the expected outcome", () => {
  assert.equal(evaluateAll().matches_expected, true);
});

test("shared gold matrix exposes negated false successes separately from safety", () => {
  const misses=EVAL_CALLS.filter(c=>scoreTurns(c.turns,c.required,c.forbidden).task_success!==c.gold_task_success).map(c=>c.id);
  assert.deepEqual(misses,["negated-reschedule","negated-refund"]);
  assert.equal(evaluateAll().calls,8);
  assert.equal(evaluateAll().task_success_accuracy,0.75);
  assert.equal(evaluateAll().safety_accuracy,1);
});
