// Route a support message to an intent using keyword-overlap scoring.

const STOPWORDS = new Set(
  (
    "a an and are as at be by can do does for from has have how i in is it its of on or " +
    "our that the their this to was we what when where which who why will with you your"
  ).split(" ")
);

function stem(token: string): string {
  for (const suffix of ["ing", "ed", "es", "s"]) {
    if (token.length > suffix.length + 2 && token.endsWith(suffix)) {
      token = token.slice(0, -suffix.length);
      break;
    }
  }
  return token.length > 3 && token.endsWith("e") ? token.slice(0, -1) : token;
}

export function tokenize(text: string): string[] {
  const matches = text.toLowerCase().match(/[a-z0-9]+/g) ?? [];
  return matches.map(stem).filter((t) => !STOPWORDS.has(t));
}

const INTENTS: Record<string, Set<string>> = {
  greeting: new Set(["hi", "hello", "hey", "greetings"]),
  goodbye: new Set(["bye", "goodbye", "farewell", "thanks", "thank"]),
  billing_question: new Set(["invoice", "charge", "bill", "billing", "payment", "refund", "price"]),
  cancel_request: new Set(["cancel", "unsubscribe", "terminate", "close"]),
  technical_issue: new Set(["error", "bug", "crash", "broken", "not", "working", "fail", "log in"]),
};
const FALLBACK = "unknown";

export function route(text: string): string {
  const tokens = new Set(tokenize(text));
  const phraseTokens = (text.toLowerCase().match(/[a-z0-9]+/g) ?? []).map(stem);
  let bestIntent = FALLBACK;
  let bestScore = 0;
  for (const [intent, keywords] of Object.entries(INTENTS)) {
    const normalized = new Set([...keywords].map((keyword) =>
      (keyword.match(/[a-z0-9]+/g) ?? []).map(stem).join(" ")));
    const score = [...normalized].filter((keyword) => {
      const parts = keyword.split(" ");
      if (parts.length === 1) return tokens.has(parts[0]);
      return phraseTokens.some((_, index) =>
        phraseTokens.slice(index, index + parts.length).join(" ") === keyword);
    }).length;
    if (score > bestScore) {
      bestIntent = intent;
      bestScore = score;
    }
  }
  return bestIntent;
}

export interface EvalCase {
  text: string;
  intent: string;
}

export const EVAL_CASES: EvalCase[] = [
  { text: "my card was charged twice", intent: "billing_question" },
  { text: "I can't log in", intent: "technical_issue" },
  { text: "Hi there, how are you?", intent: "greeting" },
  { text: "I want to cancel my subscription", intent: "cancel_request" },
  { text: "The app keeps crashing and showing an error", intent: "technical_issue" },
  { text: "What's your refund policy for canceled orders?", intent: "billing_question" },
  { text: "Thanks so much, goodbye!", intent: "goodbye" },
  { text: "asdkj qwleoi zzxcv", intent: "unknown" },
];

export function evaluateAll() {
  const correct = EVAL_CASES.filter((c) => route(c.text) === c.intent).length;
  return { cases: EVAL_CASES.length, routing_accuracy: correct / EVAL_CASES.length };
}
