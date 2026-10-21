import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, extract, score } from "./app.js";

test("ISO dates do not require or consume a following day number", () => {
  for (const text of ["Due 2026-10-16.", "Due 2026-10-16 12 items", "2026-10-16 and January 5, 2026"]) {
    const dates = extract(text).filter(e => e.type === "DATE");
    const expected = ["2026-10-16", ...(text.includes("January") ? ["January 5, 2026"] : [])];
    assert.deepEqual(dates.map(e => e.text), expected);
    assert.deepEqual(dates.map(e => text.slice(e.start, e.end)), expected);
  }
});

test("extracts person, date, and money", () => {
  const entities = extract("Jane Doe signed the contract on January 5, 2026 for $1,200.");
  const types = entities.map((e) => e.type);
  assert.ok(types.includes("PERSON"));
  assert.ok(types.includes("DATE"));
  assert.ok(types.includes("MONEY"));
});

test("score computes precision/recall/f1", () => {
  const predicted = [{ text: "Jane Doe", type: "PERSON" as const, start: 0, end: 8 }];
  const gold = [{ text: "Jane Doe", type: "PERSON" as const, start: 0, end: 8 }];
  const result = score(predicted, gold);
  assert.equal(result.f1, 1);
});

test("evaluation reports sensible metrics", () => {
  const metrics = evaluateAll();
  assert.ok(metrics.micro_like_average_f1 > 0.5);
});
