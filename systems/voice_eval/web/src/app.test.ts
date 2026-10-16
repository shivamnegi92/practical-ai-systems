import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, scoreTurns, SAMPLE_TURNS } from "./app.js";

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
  assert.equal(result.median_latency_ms, 535);
});

test("median excludes callers and missing values for even, odd and empty samples", () => {
  for (const [values, expected] of [[[0, 1], .5], [[30, 10, 20], 20], [[7], 7], [[], null]] as const) {
    const result = scoreTurns([
      { speaker: "caller", latency_ms: 99999 },
      ...values.map((latency_ms) => ({ speaker: "agent" as const, latency_ms })),
      { speaker: "agent" },
    ], []);
    assert.equal(result.median_latency_ms, expected);
  }
});
test("evaluation matches the expected outcome", () => {
  assert.equal(evaluateAll().matches_expected, true);
});
