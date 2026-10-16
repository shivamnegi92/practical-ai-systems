// Normalize OCR line records and extract conservative key/value fields.
// OCR itself is not run; input is already text + bounding boxes.

export interface OcrLine {
  text: string;
  bbox: [number, number, number, number];
}

export function normalizeLines(lines: Array<{ text?: unknown; bbox?: unknown }>): OcrLine[] {
  const out: OcrLine[] = [];
  for (const line of lines) {
    const text = String(line.text ?? "").split(/\s+/).filter(Boolean).join(" ");
    const box = line.bbox;
    if (!text || !Array.isArray(box) || box.length !== 4) continue;
    const [x1, y1, x2, y2] = box;
    if (!box.every((v) => typeof v === "number" && Number.isFinite(v)) || x2 < x1 || y2 < y1) continue;
    out.push({ text, bbox: [x1, y1, x2, y2] });
  }
  return out.sort((a, b) => Math.round(a.bbox[1] * 1000) - Math.round(b.bbox[1] * 1000) || a.bbox[0] - b.bbox[0]);
}

export function extractFields(lines: Array<{ text?: unknown; bbox?: unknown }>): Record<string, string | null> {
  const text = normalizeLines(lines).map((l) => l.text).join("\n");
  const patterns: Record<string, RegExp> = {
    invoice_number: /Invoice\s*(?:No\.?|#)?\s*:?\s*([A-Z0-9-]+)/i,
    date: /\b(\d{4}-\d{2}-\d{2})\b/,
    total: /Total\s*:?\s*\$?\s*([\d,]+\.\d{2})/i,
  };
  const result: Record<string, string | null> = {};
  for (const [key, pattern] of Object.entries(patterns)) {
    const match = pattern.exec(text);
    result[key] = match ? match[1] : null;
  }
  return result;
}

export interface EvalCase {
  lines: Array<{ text: string; bbox: [number, number, number, number] }>;
  gold: Record<string, string | null>;
}

export const EVAL_CASES: EvalCase[] = [
  {
    lines: [
      { text: "Invoice #", bbox: [0, 0, 60, 10] },
      { text: "INV-1001", bbox: [70, 0, 130, 10] },
      { text: "Total: $108.00", bbox: [0, 20, 100, 30] },
      { text: "Date: 2026-01-15", bbox: [0, 10, 100, 20] },
    ],
    gold: { invoice_number: "INV-1001", date: "2026-01-15", total: "108.00" },
  },
];

export function evaluateAll() {
  const scores = EVAL_CASES.map((c) => {
    const got = extractFields(c.lines);
    const keys = Object.keys(c.gold);
    const matches = keys.filter((k) => got[k] === c.gold[k]).length;
    return keys.length ? matches / keys.length : 0;
  });
  const mean = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
  return { documents: EVAL_CASES.length, field_exact_match: mean };
}
