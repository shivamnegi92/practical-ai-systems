// Rule-based extraction of a small, explicit invoice schema from text.

export interface Invoice {
  vendor: string | null;
  invoice_number: string | null;
  invoice_date: string | null;
  subtotal: string | null;
  tax: string | null;
  total: string | null;
  errors: string[];
}

const MONEY = String.raw`\$?\s*([0-9,]+\.\d{2})`;

function one(text: string, pattern: string): string | null {
  const match = new RegExp(pattern, "im").exec(text);
  return match ? match[1].trim() : null;
}

function isValidIsoDate(value: string): boolean {
  const d = new Date(value + "T00:00:00Z");
  return !Number.isNaN(d.getTime()) && d.toISOString().slice(0, 10) === value;
}

export function extract(text: string): Invoice {
  const invoice: Invoice = {
    vendor: one(text, "^Vendor:\\s*(.+)$"),
    invoice_number: one(text, "^Invoice(?:\\s+(?:No\\.?|Number))?:\\s*([\\w-]+)"),
    invoice_date: one(text, "^Date:\\s*(\\d{4}-\\d{2}-\\d{2})"),
    subtotal: one(text, "^Subtotal:\\s*" + MONEY),
    tax: one(text, "^Tax:\\s*" + MONEY),
    total: one(text, "^Total:\\s*" + MONEY),
    errors: [],
  };
  for (const field of ["vendor", "invoice_number", "invoice_date", "subtotal", "tax", "total"] as const) {
    if (invoice[field] === null) invoice.errors.push(`missing:${field}`);
  }
  if (invoice.invoice_date && !isValidIsoDate(invoice.invoice_date)) {
    invoice.errors.push("invalid:invoice_date");
  }
  if (invoice.subtotal && invoice.tax && invoice.total) {
    // The extractor returns two-decimal strings; integer cents avoid float rounding.
    const cents = (value: string) => BigInt(value.replace(/,/g, "").replace(".", ""));
    const subtotal = cents(invoice.subtotal);
    const tax = cents(invoice.tax);
    const total = cents(invoice.total);
    if (subtotal + tax !== total) invoice.errors.push("mismatch:total");
  }
  return invoice;
}

export interface EvalCase {
  text: string;
  fields: Partial<Record<keyof Invoice, string | null>>;
  valid: boolean;
}

export const EVAL_CASES: EvalCase[] = [
  {
    text: "Vendor: Acme Corp\nInvoice No: INV-1001\nDate: 2026-01-15\nSubtotal: 100.00\nTax: 8.00\nTotal: 108.00\n",
    fields: { vendor: "Acme Corp", total: "108.00" },
    valid: true,
  },
  {
    text: "Vendor: Beta LLC\nInvoice: INV-2002\nDate: 2026-02-01\nSubtotal: 50.00\nTax: 5.00\nTotal: 60.00\n",
    fields: { vendor: "Beta LLC" },
    valid: false,
  },
  {
    text: "Vendor: Gamma Inc\nInvoice: INV-3003\nDate: 2026-13-40\nSubtotal: 20.00\nTax: 2.00\nTotal: 22.00\n",
    fields: { vendor: "Gamma Inc" },
    valid: false,
  },
  {
    text: "Invoice: INV-4004\nDate: 2026-03-01\nSubtotal: 10.00\nTax: 1.00\nTotal: 11.00\n",
    fields: { vendor: null },
    valid: false,
  },
];

export function evaluateAll() {
  let total = 0;
  let correct = 0;
  let validTp = 0, validFp = 0, validFn = 0;
  for (const c of EVAL_CASES) {
    const got = extract(c.text);
    for (const [key, expected] of Object.entries(c.fields)) {
      total++;
      if (got[key as keyof Invoice] === expected) correct++;
    }
    const predicted = got.errors.length === 0;
    if (predicted && c.valid) validTp++;
    else if (predicted && !c.valid) validFp++;
    else if (!predicted && c.valid) validFn++;
  }
  return {
    cases: EVAL_CASES.length,
    field_exact_match: total ? correct / total : 0,
    validity_precision: validTp + validFp ? validTp / (validTp + validFp) : 0,
    validity_recall: validTp + validFn ? validTp / (validTp + validFn) : 0,
  };
}
