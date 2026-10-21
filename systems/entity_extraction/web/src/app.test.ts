import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, extract, score } from "./app.js";

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
test("money excludes trailing list comma", () => {
  const money = extract("Fees were $500, $1,200, and $75.").filter((e) => e.type === "MONEY").map((e) => e.text);
  assert.deepEqual(money, ["$500", "$1,200", "$75"]);
});
