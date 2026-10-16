// Two-stage triage -> specialist handoff with escalation for low-confidence requests.
// A triage step scores the request against fixed keyword sets per category.
// Anything with zero or too few keyword matches escalates to a human.

const STOPWORDS = new Set(
  (
    "a an and are as at be by can do does for from has have how i in is it its of on or " +
    "our that the their this to was we what when where which who why will with you your"
  ).split(" ")
);

function stem(token: string): string {
  for (const suffix of ["ing", "ed", "es", "s"]) {
    if (token.length > suffix.length + 2 && token.endsWith(suffix)) return token.slice(0, -suffix.length);
  }
  return token;
}

export function tokenize(text: string): string[] {
  const matches = text.toLowerCase().match(/[a-z0-9]+/g) ?? [];
  return matches.map(stem).filter((t) => !STOPWORDS.has(t));
}

const CATEGORIES: Record<string, Set<string>> = {
  billing: new Set(["invoice", "charge", "refund", "payment", "price"]),
  technical: new Set(["error", "bug", "crash", "broken", "login"]),
  account: new Set(["password", "delete", "username", "profile"]),
};
const CONFIDENCE_THRESHOLD = 2;
const SPECIALISTS: Record<string, () => Record<string, string>> = {
  billing: () => ({ resolution: "routed to billing specialist" }),
  technical: () => ({ resolution: "routed to technical specialist" }),
  account: () => ({ resolution: "routed to account specialist" }),
};

export function triage(text: string): [string | null, number] {
  const tokens = new Set(tokenize(text));
  let bestCategory: string | null = null;
  let bestScore = -1;
  let tied = false;
  for (const [category, keywords] of Object.entries(CATEGORIES)) {
    const score = [...tokens].filter((t) => keywords.has(t)).length;
    if (score > bestScore) {
      bestScore = score;
      bestCategory = category;
      tied = false;
    } else if (score === bestScore) {
      tied = true;
    }
  }
  return bestScore > 0 ? [tied ? null : bestCategory, bestScore] : [null, 0];
}

export function handle(request: { text: string }) {
  const [category, confidence] = triage(request.text);
  if (category === null || confidence < CONFIDENCE_THRESHOLD) {
    return { status: "escalated", category, confidence };
  }
  return { status: "resolved", category, confidence, ...SPECIALISTS[category]() };
}

export interface EvalCase { text: string; expectStatus: string; expectCategory: string | null }
export const EVAL_CASES: EvalCase[] = [
  { text: "I was charged for my invoice payment", expectStatus: "resolved", expectCategory: "billing" },
  { text: "The app keeps crashing with a login error", expectStatus: "resolved", expectCategory: "technical" },
  { text: "I need to delete my profile and change my username", expectStatus: "resolved", expectCategory: "account" },
  { text: "Hello there", expectStatus: "escalated", expectCategory: null },
  { text: "There's a bug somewhere", expectStatus: "escalated", expectCategory: "technical" },
];

export function evaluateAll() {
  const correct = EVAL_CASES.filter((c) => {
    const result = handle({ text: c.text });
    return result.status === c.expectStatus && result.category === c.expectCategory;
  }).length;
  return { cases: EVAL_CASES.length, routing_accuracy: correct / EVAL_CASES.length };
}
