import { test } from "node:test";
import { strict as assert } from "node:assert";
import { detect, evaluateAll, redact } from "./app.js";

test("detects email", () => {
  const findings = detect("Contact jane.doe@example.com for help.");
  assert.deepEqual(findings.map((f) => f.type), ["email"]);
});

test("redacts matches in place", () => {
  const redacted = redact("Call (555) 123-4567 now.");
  assert.ok(!redacted.includes("123-4567"));
  assert.ok(redacted.includes("[REDACTED:PHONE]"));
});

test("clean text has no findings", () => {
  assert.deepEqual(detect("No personal data here, just a meeting at 3pm."), []);
});

test("ssn pattern does not also match as phone", () => {
  const findings = detect("SSN on file: 123-45-6789.");
  assert.deepEqual(findings.map((f) => f.type), ["ssn"]);
});

test("expanded evaluation includes the documented phone misses", () => {
  const result=evaluateAll();
  assert.equal(result.cases,7);
  assert.equal(result.precision,1);
  assert.equal(result.recall,2/3);
  assert.equal(result.f1,0.8);
});

test("parenthesized area code is fully redacted", () => {
  assert.equal(redact("Call (555) 123-4567 now."), "Call [REDACTED:PHONE] now.");
});

test("dashed phone is fully redacted", () => {
  assert.equal(redact("Call 555-123-4567 now."), "Call [REDACTED:PHONE] now.");
});
