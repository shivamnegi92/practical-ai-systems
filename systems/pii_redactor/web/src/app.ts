// Detect and redact a small set of obvious PII patterns in text.
// Pattern matching only -- not an entity-recognition model, not a compliance tool.

export interface Finding {
  type: string;
  match: string;
  start: number;
  end: number;
}

const PATTERNS: Array<[string, RegExp]> = [
  ["email", /\b[\w.+-]+@[\w-]+\.[\w.-]+\b/g],
  ["phone", /(?<!\w)(?:\+?1[-.\s]?)?(?:\(\d{3}\)\s?|\d{3}[-.\s])\d{3}[-.\s]\d{4}\b/g],
  ["ssn", /\b\d{3}-\d{2}-\d{4}\b/g],
  ["credit_card", /\b(?:\d{4}[-\s]){3}\d{4}\b/g],
];

export function detect(text: string): Finding[] {
  const findings: Finding[] = [];
  for (const [type, pattern] of PATTERNS) {
    const re = new RegExp(pattern.source, pattern.flags);
    let match: RegExpExecArray | null;
    while ((match = re.exec(text)) !== null) {
      findings.push({ type, match: match[0], start: match.index, end: match.index + match[0].length });
    }
  }
  return findings.sort((a, b) => a.start - b.start);
}

export function redact(text: string): string {
  // Merge original spans before replacement shifts offsets. Earliest match
  // labels the union; a shared start prefers the longest match.
  const spans: Finding[] = [];
  for (const f of detect(text).sort((a, b) => a.start - b.start || b.end - a.end)) {
    const previous = spans[spans.length - 1];
    if (previous && f.start < previous.end) previous.end = Math.max(previous.end, f.end);
    else spans.push({ ...f });
  }
  for (const f of spans.reverse()) {
    text = text.slice(0, f.start) + `[REDACTED:${f.type.toUpperCase()}]` + text.slice(f.end);
  }
  return text;
}

export interface EvalCase {
  text: string;
  gold_types: string[];
}

export const EVAL_CASES: EvalCase[] = [
  { text: "Contact me at jane.doe@example.com for details.", gold_types: ["email"] },
  { text: "Call us at (555) 123-4567 anytime.", gold_types: ["phone"] },
  { text: "SSN on file: 123-45-6789.", gold_types: ["ssn"] },
  { text: "No personal data here, just a meeting at 3pm.", gold_types: [] },
  { text: "Card number 4111-1111-1111-1111 was used.", gold_types: ["credit_card"] },
];

export function evaluateAll() {
  let tp = 0, fp = 0, fn = 0;
  for (const c of EVAL_CASES) {
    const predicted = new Set(detect(c.text).map((f) => f.type));
    const gold = new Set(c.gold_types);
    for (const t of predicted) if (gold.has(t)) tp++; else fp++;
    for (const t of gold) if (!predicted.has(t)) fn++;
  }
  const precision = tp + fp ? tp / (tp + fp) : 0;
  const recall = tp + fn ? tp / (tp + fn) : 0;
  const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
  return { cases: EVAL_CASES.length, precision, recall, f1 };
}
