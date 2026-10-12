// Lexicon-based positive/negative/neutral sentiment classifier.
// No stemming or embeddings; ties between positive/negative resolve to neutral.

const POSITIVE = new Set(["good", "great", "excellent", "love", "loved", "loves", "happy", "amazing", "fantastic", "wonderful", "easy", "fast"]);
const NEGATIVE = new Set(["bad", "terrible", "hate", "hated", "hates", "slow", "broken", "awful", "horrible", "worst", "confusing", "frustrating"]);

function words(text: string): string[] {
  return text.toLowerCase().replace(/\u2019/g, "'").match(/[a-z]*n't|[a-z]+/g) ?? [];
}

export function classify(text: string): "positive" | "negative" | "neutral" {
  const ws = words(text);
  let score = 0;
  for (let i = 0; i < ws.length; i++) {
    const polarity = Number(POSITIVE.has(ws[i])) - Number(NEGATIVE.has(ws[i]));
    const negated = ws.slice(Math.max(0, i - 3), i).some((token) =>
      ["not", "never", "no", "n't"].includes(token) || token.endsWith("n't"));
    score += negated ? -polarity : polarity;
  }
  if (score > 0) return "positive";
  if (score < 0) return "negative";
  return "neutral";
}

export interface EvalCase {
  text: string;
  label: string;
}

export const EVAL_CASES: EvalCase[] = [
  { text: "This is not good", label: "negative" },
  { text: "not bad at all", label: "positive" },
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
