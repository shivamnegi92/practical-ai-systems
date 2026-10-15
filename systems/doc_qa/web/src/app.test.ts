import { test } from "node:test";
import { strict as assert } from "node:assert";
import { CHUNKS, DocQA, evaluateAll } from "./app.js";

test("answers with citation", () => {
  const qa = new DocQA(CHUNKS);
  const answer = qa.answer("How much does the Pro plan cost?");
  assert.ok(answer.text.includes("$8"));
  assert.equal(answer.citations[0], "billing.md#1");
  assert.equal(answer.abstained, false);
});

test("abstains when there is no evidence", () => {
  const qa = new DocQA(CHUNKS);
  const answer = qa.answer("Does the app integrate with Salesforce CRM?");
  assert.equal(answer.abstained, true);
  assert.deepEqual(answer.citations, []);
});

test("evaluation metrics are in a reasonable range", () => {
  const metrics = evaluateAll();
  assert.ok(metrics.recall_at_3 >= 0.6);
  assert.ok(metrics.correct_abstention_rate >= 0.5);
});

test("shared qualifier cases expose the web future-price miss", () => {
  const qa = new DocQA(CHUNKS);
  assert.equal(qa.answer("What is the price of the Pro plan in 2035?").abstained, false);
  assert.equal(qa.answer("How much does the Pro plan cost in Japanese yen?").abstained, true);
  for (const question of ["How many days is version history kept on the Enterprise plan?", "How long are reset links valid after five failed sign-in attempts?"]) assert.equal(qa.answer(question).abstained, true);
  assert.equal(evaluateAll().cases, 26);
  assert.equal(evaluateAll().correct_abstention_rate, 0.875);
});
