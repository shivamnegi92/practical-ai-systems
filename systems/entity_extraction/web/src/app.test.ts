import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, extract, score } from "./app.js";

test("known places keep exact spans and person labels", () => {
  for (const place of ["New York", "San Francisco", "Los Angeles", "New Delhi", "New  York"]) {
    const text = `Meeting in ${place} with Dr. Ana Li.`;
    const entities = extract(text);
    assert.ok(entities.some((e) => e.text === place && e.type === "LOCATION" && e.start === 11 && e.end === 11 + place.length));
    assert.ok(entities.some((e) => e.text === "Ana Li" && e.type === "PERSON"));
    assert.deepEqual(entities.map((e) => text.slice(e.start, e.end)), entities.map((e) => e.text));
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
