import { test } from "node:test";

test("requires a whole ISO calendar date field", () => {
  for (const value of ["2026-01-010", "2026-01-01junk", "2026-01-01T10:00:00", "", "\n2026-01-01"]) {
    const result = extract("Date: " + value + "\nVendor: Demo\n");
    assert.equal(result.invoice_date, null);
    assert.ok(result.errors.includes("missing:invoice_date"));
  }
  for (const value of ["0001-01-01", "9999-12-31", "2024-02-29"]) {
    for (const newline of ["\n", "\r\n"]) {
      const result = extract("Date:\t" + value + " \t" + newline);
      assert.equal(result.invoice_date, value);
      assert.equal(result.errors.includes("invalid:invoice_date"), false);
    }
  }
  assert.ok(extract("Date: 0000-01-01\n").errors.includes("invalid:invoice_date"));
  assert.ok(extract("Date: 2026-02-29\n").errors.includes("invalid:invoice_date"));
});
import { strict as assert } from "node:assert";
import { evaluateAll, extract } from "./app.js";

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
