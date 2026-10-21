// Detect near-duplicate questions using token Jaccard similarity.

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
  return matches.filter((t) => !STOPWORDS.has(t)).map(stem);
}

export function similarity(a: string, b: string): number {
  const ta = new Set(tokenize(a));
  const tb = new Set(tokenize(b));
  if (ta.size === 0 && tb.size === 0) return 1;
  if (ta.size === 0 || tb.size === 0) return 0;
  const intersection = [...ta].filter((t) => tb.has(t)).length;
  const union = new Set([...ta, ...tb]).size;
  return intersection / union;
}

export function findDuplicates(questions: string[], threshold = 0.6): Array<[number, number, number]> {
  const pairs: Array<[number, number, number]> = [];
  for (let i = 0; i < questions.length; i++) {
    for (let j = i + 1; j < questions.length; j++) {
      const score = similarity(questions[i], questions[j]);
      if (score >= threshold) pairs.push([i, j, Math.round(score * 10000) / 10000]);
    }
  }
  return pairs;
}

export interface EvalCase {
  a: string;
  b: string;
  duplicate: boolean;
}

export const EVAL_CASES: EvalCase[] = [
  { a: "How do I reset my password?", b: "How can I reset my password?", duplicate: true },
  { a: "What is your refund policy?", b: "What is your return policy?", duplicate: false },
  { a: "Where is my order?", b: "Track my order status", duplicate: false },
  { a: "Cancel my subscription please", b: "I want to cancel my subscription", duplicate: true },
  { a: "What time do you open?", b: "What's your return policy?", duplicate: false },
];

export function evaluateAll(threshold = 0.6) {
  let tp = 0;
  let fp = 0;
  let fn = 0;
  for (const c of EVAL_CASES) {
    const predicted = similarity(c.a, c.b) >= threshold;
    if (predicted && c.duplicate) tp++;
    else if (predicted && !c.duplicate) fp++;
    else if (!predicted && c.duplicate) fn++;
  }
  const precision = tp + fp ? tp / (tp + fp) : 0;
  const recall = tp + fn ? tp / (tp + fn) : 0;
  const f1 = precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
  return { cases: EVAL_CASES.length, precision, recall, f1 };
}
