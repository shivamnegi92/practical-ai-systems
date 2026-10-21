// Lexicon-based positive/negative/neutral sentiment classifier.
// No stemming or embeddings; ties between positive/negative resolve to neutral.

const POSITIVE = new Set(["good", "great", "excellent", "love", "loved", "loves", "happy", "amazing", "fantastic", "wonderful", "easy", "fast"]);
const NEGATIVE = new Set(["bad", "terrible", "hate", "hated", "hates", "slow", "broken", "awful", "horrible", "worst", "confusing", "frustrating"]);

function words(text: string): string[] {
  return text.toLowerCase().match(/[a-z]+/g) ?? [];
}

export function classify(text: string): "positive" | "negative" | "neutral" {
  if (typeof text !== "string") {
    throw new TypeError(`text must be a string, got ${typeof text}`);
  }
  const ws = words(text);
  const positive = ws.filter((w) => POSITIVE.has(w)).length;
  const negative = ws.filter((w) => NEGATIVE.has(w)).length;
  if (positive > negative) return "positive";
  if (negative > positive) return "negative";
  return "neutral";
}

export interface EvalCase {
  text: string;
  label: string;
}

export const EVAL_CASES: EvalCase[] = [
  { text: "This product is great and the support team is fantastic.", label: "positive" },
  { text: "The checkout process is slow and confusing.", label: "negative" },
  { text: "It's okay, does the job.", label: "neutral" },
  { text: "I love this app but the login page is terrible.", label: "neutral" },
  { text: "Absolutely amazing experience, wonderful service, fast delivery!", label: "positive" },
];

export function evaluateAll() {
  const correct = EVAL_CASES.filter((c) => classify(c.text) === c.label).length;
  return { cases: EVAL_CASES.length, accuracy: correct / EVAL_CASES.length };
}
