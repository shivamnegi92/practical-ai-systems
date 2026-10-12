// Find names, dates, and amounts in business text using explicit patterns.

export interface Entity {
  text: string;
  type: "PERSON" | "LOCATION" | "DATE" | "MONEY";
  start: number;
  end: number;
}

const PATTERNS: Array<[Entity["type"], RegExp]> = [
  ["PERSON", /\b[A-Z][a-z]+\s+[A-Z][a-z]+\b/g],
  [
    "DATE",
    /\b(?:\d{4}-\d{2}-\d{2}|Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:,?\s+\d{4})?\b/gi,
  ],
  ["MONEY", /\$\s?\d[\d,]*(?:\.\d{2})?/g],
];
const PLACES = new Set(["new york", "san francisco", "los angeles", "new delhi"]);

export function extract(text: string): Entity[] {
  const entities: Entity[] = [];
  for (const [type, pattern] of PATTERNS) {
    const re = new RegExp(pattern.source, pattern.flags);
    let match: RegExpExecArray | null;
    while ((match = re.exec(text)) !== null) {
      const kind = type === "PERSON" && PLACES.has(match[0].toLowerCase().split(/\s+/).join(" ")) ? "LOCATION" : type;
      entities.push({ text: match[0], type: kind, start: match.index, end: match.index + match[0].length });
    }
  }
  return entities.sort((a, b) => a.start - b.start || a.end - b.end || a.type.localeCompare(b.type));
}

function prf(tp: number, fp: number, fn: number) {
  const precision = tp + fp ? tp / (tp + fp) : 0;
  const recall = tp + fn ? tp / (tp + fn) : 0;
  const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
  return { precision, recall, f1 };
}

export function score(predicted: Entity[], gold: Entity[]) {
  const p = new Set(predicted.map((e) => `${e.text}\u0000${e.type}`));
  const g = new Set(gold.map((e) => `${e.text}\u0000${e.type}`));
  const tp = [...p].filter((x) => g.has(x)).length;
  return prf(tp, p.size - tp, g.size - tp);
}

export interface EvalCase {
  text: string;
  gold: Entity[];
}

export const EVAL_CASES: EvalCase[] = [
  {
    text: "Meeting in New York with Dr. Ana Li.",
    gold: [{ text: "New York", type: "LOCATION", start: 11, end: 19 }, { text: "Ana Li", type: "PERSON", start: 29, end: 35 }],
  },
  { text: "Our office is in San Francisco.", gold: [{ text: "San Francisco", type: "LOCATION", start: 17, end: 30 }] },
  { text: "Travel to Los Angeles.", gold: [{ text: "Los Angeles", type: "LOCATION", start: 10, end: 21 }] },
  // Known miss: outside the small gazetteer; keep the correct gold label.
  { text: "Visit Buenos Aires.", gold: [{ text: "Buenos Aires", type: "LOCATION", start: 6, end: 18 }] },
  {
    text: "Jane Doe signed the contract on January 5, 2026 for $1,200.",
    gold: [
      { text: "Jane Doe", type: "PERSON", start: 0, end: 8 },
      { text: "January 5, 2026", type: "DATE", start: 29, end: 44 },
      { text: "$1,200", type: "MONEY", start: 53, end: 59 },
    ],
  },
  {
    text: "Invoice total: $450.00. Contact John Smith.",
    gold: [
      { text: "$450.00", type: "MONEY", start: 15, end: 22 },
      { text: "John Smith", type: "PERSON", start: 33, end: 43 },
    ],
  },
];

export function evaluateAll() {
  const scores = EVAL_CASES.map((c) => score(extract(c.text), c.gold));
  const mean = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0);
  return {
    cases: EVAL_CASES.length,
    micro_like_average_precision: mean(scores.map((s) => s.precision)),
    micro_like_average_recall: mean(scores.map((s) => s.recall)),
    micro_like_average_f1: mean(scores.map((s) => s.f1)),
  };
}
