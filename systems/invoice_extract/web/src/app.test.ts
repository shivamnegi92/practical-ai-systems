import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, extract } from "./app.js";

test("US thousands separators preserve fields and validate balance", () => {
  const text = "Vendor: A\nInvoice: 1\nDate: 2026-01-01\nSubtotal: 1,000.00\nTax: 80.00\nTotal: 1,080.00";
  const invoice = extract(text);
  assert.equal(invoice.subtotal, "1,000.00");
  assert.equal(invoice.total, "1,080.00");
  assert.deepEqual(invoice.errors, []);
  assert.deepEqual(extract(text.replace("1,080.00", "1,090.00")).errors, ["mismatch:total"]);
});

test("extracts a clean invoice with matching total", () => {
  const text = "Vendor: Acme Corp\nInvoice No: INV-1001\nDate: 2026-01-15\nSubtotal: 100.00\nTax: 8.00\nTotal: 108.00\n";
  const invoice = extract(text);
  assert.equal(invoice.vendor, "Acme Corp");
  assert.deepEqual(invoice.errors, []);
});

test("flags a total mismatch", () => {
  const text = "Vendor: Beta LLC\nInvoice: INV-2002\nDate: 2026-02-01\nSubtotal: 50.00\nTax: 5.00\nTotal: 60.00\n";
  const invoice = extract(text);
  assert.ok(invoice.errors.includes("mismatch:total"));
});

test("flags an invalid date", () => {
  const text = "Vendor: Gamma Inc\nInvoice: INV-3003\nDate: 2026-13-40\nSubtotal: 20.00\nTax: 2.00\nTotal: 22.00\n";
  assert.ok(extract(text).errors.includes("invalid:invoice_date"));
});

test("flags a missing field", () => {
  const text = "Invoice: INV-4004\nDate: 2026-03-01\nSubtotal: 10.00\nTax: 1.00\nTotal: 11.00\n";
  assert.ok(extract(text).errors.includes("missing:vendor"));
});

test("evaluation reports sensible metrics", () => {
  const metrics = evaluateAll();
  assert.ok(metrics.field_exact_match > 0.5);
});
