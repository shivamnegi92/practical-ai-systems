// Document Q&A with citations and abstention: BM25 retrieval + extractive answer.
// Standalone: zero runtime dependencies; sample docs are embedded below (see
// ../data/*.md for the source files this was generated from).

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

export function sentences(text: string): string[] {
  return text.trim().split(/(?<=[.!?])\s+/).map((s) => s.trim()).filter(Boolean);
}

export class BM25 {
  tokens: Record<string, string[]> = Object.create(null);
  avgLen: number;
  idf: Record<string, number> = {};

  constructor(private docs: Record<string, string>, private k1 = 1.5, private b = 0.75) {
    for (const [id, text] of Object.entries(docs)) this.tokens[id] = tokenize(text);
    const lens = Object.values(this.tokens).map((t) => t.length);
    this.avgLen = lens.length ? lens.reduce((a, b2) => a + b2, 0) / lens.length : 0;
    const df = new Map<string, number>();
    for (const toks of Object.values(this.tokens)) {
      for (const term of new Set(toks)) df.set(term, (df.get(term) ?? 0) + 1);
    }
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
    return scored
      .filter(([, s]) => s > 0)
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, k);
  }
}

const ABSTAIN = "I can't find that in the documentation.";

export const CHUNKS: Record<string, string> = {
  "accounts.md#1":
    'To reset your password, open the sign-in page, choose "Forgot password", and follow the link sent to your email. Reset links expire after 30 minutes.',
  "accounts.md#2":
    "Two-factor authentication can be enabled under Settings > Security. Lumen Notes supports authenticator apps and hardware security keys, but not SMS codes.",
  "accounts.md#3":
    "If you lose access to your two-factor device, use one of the ten recovery codes generated during setup. Each recovery code works only once.",
  "accounts.md#4":
    "Accounts that stay inactive for 24 months are scheduled for deletion. We email the account owner 30 days before deletion.",
  "billing.md#1":
    "The Free plan includes up to 3 notebooks and 500 MB of storage. The Pro plan costs $8 per user per month and removes notebook limits.",
  "billing.md#2": "Annual Pro subscriptions receive a 20 percent discount compared with monthly billing.",
  "billing.md#3":
    "You can cancel a subscription at any time from Settings > Billing. Cancellation takes effect at the end of the current billing period, and unused time is not refunded.",
  "billing.md#4":
    "Invoices are emailed to the billing contact on the first day of each billing cycle. Past invoices can be downloaded as PDF files from the billing page.",
  "sharing.md#1":
    "You can share a notebook by email invitation or with a view-only public link. Public links can be disabled at any time, which immediately revokes access.",
  "sharing.md#2": "Collaborators on the Pro plan can comment and edit. Free plan collaborators can only view and comment.",
  "sharing.md#3":
    "Version history keeps every saved revision for 90 days on Pro and 7 days on Free. You can restore any revision from the note menu.",
  "sharing.md#4":
    "Exports are available as Markdown, PDF, or HTML. Exporting an entire workspace is limited to workspace administrators.",
  "sync.md#1":
    "Notes sync automatically every 60 seconds while you are online. You can force a sync by pressing Ctrl+S on desktop or pulling down on the mobile notes list.",
  "sync.md#2":
    "Offline mode keeps your 50 most recently opened notebooks available on the device. Edits made offline sync when the connection returns.",
  "sync.md#3":
    "When two devices edit the same note offline, Lumen Notes keeps both versions and marks the newer one as a conflict copy for you to review.",
  "sync.md#4":
    'Attachments larger than 25 MB do not sync on mobile data unless you enable "Sync large files on cellular" in settings.',
};

export interface Answer {
  text: string;
  citations: string[];
  retrieved: string[];
  abstained: boolean;
}

export class DocQA {
  index: BM25;
  chunks: Record<string, string>;

  constructor(chunks: Record<string, string>, private minScore = 2.5, private minCoverage = 0.5, private k = 3) {
    this.chunks = chunks;
    this.index = new BM25(chunks);
  }

  retrieve(question: string) {
    return this.index.search(question, this.k);
  }

  coverage(question: string, chunkId: string): number {
    const query = new Set(tokenize(question));
    if (query.size === 0) return 0;
    const chunkTokens = new Set(this.index.tokens[chunkId]);
    return [...query].filter((t) => chunkTokens.has(t)).length / query.size;
  }

  answer(question: string): Answer {
    const hits = this.retrieve(question);
    const retrieved = hits.map(([id]) => id);
    if (hits.length === 0 || hits[0][1] < this.minScore) {
      return { text: ABSTAIN, citations: [], retrieved, abstained: true };
    }
    if (this.coverage(question, hits[0][0]) < this.minCoverage) {
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

export interface EvalCase {
  question: string;
  gold: string | null;
  expect: string | null;
}

export const EVAL_CASES: EvalCase[] = [
  { question: "How much does the Pro plan cost?", gold: "billing.md#1", expect: "$8" },
  { question: "How often do notes sync?", gold: "sync.md#1", expect: "60 seconds" },
  { question: "How do I reset my password?", gold: "accounts.md#1", expect: "Forgot password" },
  { question: "Does Lumen Notes integrate with Salesforce CRM?", gold: null, expect: null },
  { question: "Is there a student discount?", gold: null, expect: null },
];

export function evaluateAll() {
  const qa = new DocQA(CHUNKS);
  const answerable = EVAL_CASES.filter((c) => c.gold);
  const unanswerable = EVAL_CASES.filter((c) => !c.gold);
  const mean = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0);
  const recallAt3 = mean(answerable.map((c) => (qa.answer(c.question).retrieved.includes(c.gold!) ? 1 : 0)));
  const correctAbstention = mean(unanswerable.map((c) => (qa.answer(c.question).abstained ? 1 : 0)));
  return { cases: EVAL_CASES.length, recall_at_3: recallAt3, correct_abstention_rate: correctAbstention };
}
