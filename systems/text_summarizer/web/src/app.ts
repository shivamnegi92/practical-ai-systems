// Extractive summarizer: rank sentences by shared frequent-word score.
// Pure logic, no DOM/runtime dependencies -- see main.ts for the UI wiring.

const STOPWORDS = new Set(
  (
    "a an and are as at be by can do does for from has have how i in is it its of on or " +
    "our that the their this to was we what when where which who why will with you your"
  ).split(" ")
);

function stem(token: string): string {
  for (const suffix of ["ing", "ed", "es", "s"]) {
    if (token.length > suffix.length + 2 && token.endsWith(suffix)) {
      return token.slice(0, -suffix.length);
    }
  }
  return token;
}

export function tokenize(text: string): string[] {
  const matches = text.toLowerCase().match(/[a-z0-9]+/g) ?? [];
  return matches.map(stem).filter((t) => !STOPWORDS.has(t));
}

export function sentences(text: string): string[] {
  return text
    .trim()
    .split(/(?<=[.!?])\s+/)
    .map((s) => s.trim())
    .filter(Boolean);
}

export function summarize(text: string, n = 2): string[] {
  if (!Number.isInteger(n) || n < 0) throw new RangeError("n must be a nonnegative integer");
  const sents = sentences(text);
  if (sents.length <= n) return sents;
  const freq = new Map<string, number>();
  for (const t of tokenize(text)) freq.set(t, (freq.get(t) ?? 0) + 1);
  const scored = sents.map((sent, index) => {
    const terms = tokenize(sent);
    const score = terms.length ? terms.reduce((sum, t) => sum + (freq.get(t) ?? 0), 0) / terms.length : 0;
    return { score, index, sent };
  });
  const top = [...scored].sort((a, b) => b.score - a.score).slice(0, n);
  return top.sort((a, b) => a.index - b.index).map((s) => s.sent);
}

export function compressionRatio(text: string, summary: string[]): number {
  const original = text.length;
  const compressed = summary.join(" ").length;
  return original ? compressed / original : 0;
}

export interface EvalCase {
  text: string;
  key_sentence: string;
  n?: number;
}

export const EVAL_CASES: EvalCase[] = [
  {
    text: "Database indexing speeds up queries. Indexing indexing indexing is crucial for performance. The weather was nice yesterday.",
    key_sentence: "Indexing indexing indexing",
    n: 1,
  },
  {
    text: "Our office closes early on Fridays. Parking parking parking is limited downtown. The cafeteria serves lunch at noon.",
    key_sentence: "Parking parking parking",
    n: 1,
  },
  {
    text: "Rockets rockets rockets launch from the coast. The museum opens at nine. Gift shops sell postcards.",
    key_sentence: "Rockets rockets rockets",
    n: 1,
  },
  {
    text: "Onboarding onboarding onboarding takes one day. The office has a rooftop garden. Lunch is provided on Mondays.",
    key_sentence: "Onboarding onboarding onboarding",
    n: 1,
  },
  {
    text: "Glaciers glaciers glaciers are melting faster. Tourists visit the lake in summer. Local guides lead short hikes.",
    key_sentence: "Glaciers glaciers glaciers",
    n: 1,
  },
];

function mean(values: number[]): number {
  return values.length ? values.reduce((a, b) => a + b, 0) / values.length : 0;
}

export function evaluateAll() {
  const hits = EVAL_CASES.map((c) => summarize(c.text, c.n ?? 2).some((s) => s.includes(c.key_sentence)));
  const ratios = EVAL_CASES.map((c) => compressionRatio(c.text, summarize(c.text, c.n ?? 2)));
  return {
    cases: EVAL_CASES.length,
    key_sentence_recall: Math.round(mean(hits.map(Number)) * 10000) / 10000,
    avg_compression_ratio: Math.round(mean(ratios) * 10000) / 10000,
  };
}
