import { test } from "node:test";

test("overlapping email/SSN spans are replaced once using original offsets", () => {
  for (const email of ["123-45-6789@example.com","user.123-45-6789@example.com"]) {
    const text=`Contact ${email} today.`;
    assert.deepEqual(new Set(detect(text).map(f=>f.type)),new Set(["email","ssn"]));
    assert.equal(redact(text),"Contact [REDACTED:EMAIL] today.");
  }
  assert.equal(redact("📧 user.123-45-6789@example.com; SSN 987-65-4321. End."),"📧 [REDACTED:EMAIL]; SSN [REDACTED:SSN]. End.");
});
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

test("evaluation is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().f1, 1);
});

test("parenthesized area code is fully redacted", () => {
  assert.equal(redact("Call (555) 123-4567 now."), "Call [REDACTED:PHONE] now.");
});

test("dashed phone is fully redacted", () => {
  assert.equal(redact("Call 555-123-4567 now."), "Call [REDACTED:PHONE] now.");
});
