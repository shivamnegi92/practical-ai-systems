// Decompose a multi-part question and require every part to be answered before replying.
// Splits on " and " or a mid-string "?" to get sub-questions, answers each with
// a small bundled BM25 + extractive DocQA baseline (see systems/doc_qa for the
// original standalone single-hop version), and abstains for the whole question
// unless every sub-question is independently answered.

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

function tokenize(text: string): string[] {
  const matches = text.toLowerCase().match(/[a-z0-9]+/g) ?? [];
  return matches.map(stem).filter((t) => !STOPWORDS.has(t));
}

function sentences(text: string): string[] {
  return text.trim().split(/(?<=[.!?])\s+/).map((s) => s.trim()).filter(Boolean);
}

class BM25 {
  tokens: Record<string, string[]> = Object.create(null);
  avgLen: number;
  idf: Record<string, number> = {};
  constructor(docs: Record<string, string>, private k1 = 1.5, private b = 0.75) {
    for (const [id, text] of Object.entries(docs)) this.tokens[id] = tokenize(text);
    const lens = Object.values(this.tokens).map((t) => t.length);
    this.avgLen = lens.length ? lens.reduce((a, b2) => a + b2, 0) / lens.length : 0;
    const df = new Map<string, number>();
    for (const toks of Object.values(this.tokens)) for (const term of new Set(toks)) df.set(term, (df.get(term) ?? 0) + 1);
    const n = Object.keys(this.tokens).length;
    for (const [term, freq] of df) this.idf[term] = Math.log(1 + (n - freq + 0.5) / (freq + 0.5));
  }
  score(query: string, docId: string): number {
    const toks = this.tokens[docId];
    const counts = new Map<string, number>();
    for (const t of toks) counts.set(t, (counts.get(t) ?? 0) + 1);
    const norm = this.k1 * (1 - this.b + (this.b * toks.length) / (this.avgLen || 1));
    let total = 0;
    for (const t of new Set(tokenize(query))) {
      const c = counts.get(t);
      if (c) total += (this.idf[t] ?? 0) * (c * (this.k1 + 1)) / (c + norm);
    }
    return total;
  }
  search(query: string, k = 5): Array<[string, number]> {
    const scored: Array<[string, number]> = Object.keys(this.tokens).map((id) => [id, this.score(query, id)]);
    return scored.filter(([, s]) => s > 0).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, k);
  }
}

const ABSTAIN = "I can't find that in the documentation.";
const SPLIT_PATTERN = /\s+and\s+|\?\s*(?=\w)/gi;

export const CHUNKS: Record<string, string> = {
  "accounts.md#1": 'To reset your password, open the sign-in page, choose "Forgot password", and follow the link sent to your email. Reset links expire after 30 minutes.',
  "billing.md#1": "The Free plan includes up to 3 notebooks and 500 MB of storage. The Pro plan costs $8 per user per month and removes notebook limits.",
  "sync.md#1": "Notes sync automatically every 60 seconds while you are online. You can force a sync by pressing Ctrl+S on desktop or pulling down on the mobile notes list.",
};

interface Answer { text: string; citations: string[]; retrieved: string[]; abstained: boolean }

class DocQA {
  index: BM25;
  constructor(public chunks: Record<string, string>, private minScore = 2.5, private minCoverage = 0.5, private k = 3) {
    this.index = new BM25(chunks);
  }
  coverage(question: string, chunkId: string): number {
    const query = new Set(tokenize(question));
    if (query.size === 0) return 0;
    const chunkTokens = new Set(this.index.tokens[chunkId]);
    return [...query].filter((t) => chunkTokens.has(t)).length / query.size;
  }
  answer(question: string): Answer {
    const hits = this.index.search(question, this.k);
    const retrieved = hits.map(([id]) => id);
    if (hits.length === 0 || hits[0][1] < this.minScore || this.coverage(question, hits[0][0]) < this.minCoverage) {
      return { text: ABSTAIN, citations: [], retrieved, abstained: true };
    }
    const query = new Set(tokenize(question));
    const sents = sentences(this.chunks[hits[0][0]]);
    const best = sents.reduce((bestSoFar, s) => {
      const overlap = [...query].filter((t) => tokenize(s).includes(t)).length;
      const bestOverlap = [...query].filter((t) => tokenize(bestSoFar).includes(t)).length;
      return overlap > bestOverlap ? s : bestSoFar;
    }, sents[0]);
    return { text: best, citations: [hits[0][0]], retrieved, abstained: false };
  }
}

export function decompose(question: string): string[] {
  return question
    .split(SPLIT_PATTERN)
    .map((part) => part.trim())
    .filter(Boolean)
    .map((part) => part.replace(/\?+$/, "") + "?");
}

export function answerMultiHop(question: string, qa: DocQA = new DocQA(CHUNKS)) {
  const subQuestions = decompose(question);
  const subAnswers = subQuestions.map((q) => qa.answer(q));
  if (subAnswers.some((a) => a.abstained)) {
    return { abstained: true, sub_questions: subQuestions, answer: null as string | null, citations: [] as string[] };
  }
  return {
    abstained: false,
    sub_questions: subQuestions,
    answer: subAnswers.map((a) => a.text).join(" "),
    citations: subAnswers.flatMap((a) => a.citations),
  };
}

export interface EvalCase { question: string; goldAbstained: boolean }
export const EVAL_CASES: EvalCase[] = [
  { question: "How much does the Pro plan cost and how often do notes sync?", goldAbstained: false },
  { question: "How much does the Pro plan cost and does it integrate with Salesforce CRM?", goldAbstained: true },
  { question: "How often do notes sync? How do I reset my password?", goldAbstained: false },
];

export function evaluateAll() {
  const qa = new DocQA(CHUNKS);
  const correct = EVAL_CASES.filter((c) => answerMultiHop(c.question, qa).abstained === c.goldAbstained).length;
  return { cases: EVAL_CASES.length, abstention_accuracy: correct / EVAL_CASES.length };
}
