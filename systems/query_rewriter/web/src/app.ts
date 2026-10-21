// Rule-based query expansion: add synonyms before lexical retrieval.
// Pairs a bundled BM25 index with a small synonym list to show how query
// expansion can recover queries that share no literal tokens with the
// document they need.

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

export class BM25 {
  tokens: Record<string, string[]> = {};
  avgLen: number;
  idf: Record<string, number> = {};

  constructor(private docs: Record<string, string>, private k1 = 1.5, private b = 0.75) {
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

const SYNONYMS: Record<string, string[]> = {
  price: ["cost"],
  pricing: ["cost"],
  terminate: ["cancel"],
  unsubscribe: ["cancel"],
  erase: ["delete"],
  remove: ["delete"],
};

export function expandQuery(query: string): string {
  const queryTerms = tokenize(query);
  const seen = new Set(queryTerms);
  const extra: string[] = [];
  for (const term of queryTerms) {
    for (const synonym of SYNONYMS[term] ?? []) {
      const stemmed = stem(synonym);
      if (!seen.has(stemmed) && !seen.has(synonym)) {
        seen.add(stemmed);
        seen.add(synonym);
        extra.push(synonym);
      }
    }
  }
  return extra.length ? [query, ...extra].join(" ") : query;
}

export function search(corpus: Record<string, string>, query: string, expand = false, k = 1) {
  const index = new BM25(corpus);
  return index.search(expand ? expandQuery(query) : query, k);
}

export const CORPUS: Record<string, string> = {
  d1: "Costs are eight dollars monthly.",
  d2: "We ship worldwide within five days.",
  d3: "Cancel requests take one business day.",
  d4: "Delete your account from the settings page.",
};

export interface EvalQuery { text: string; gold: string }
export const EVAL_QUERIES: EvalQuery[] = [
  { text: "What is the price?", gold: "d1" },
  { text: "How do I terminate my account?", gold: "d3" },
  { text: "How can I erase my data?", gold: "d4" },
];

export function evaluateAll() {
  const index = new BM25(CORPUS);
  const mean = (xs: number[]) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : 0);
  const baseline = EVAL_QUERIES.map((q) => {
    const hits = index.search(q.text, 1);
    return hits.length && hits[0][0] === q.gold ? 1 : 0;
  });
  const expanded = EVAL_QUERIES.map((q) => {
    const hits = index.search(expandQuery(q.text), 1);
    return hits.length && hits[0][0] === q.gold ? 1 : 0;
  });
  return {
    cases: EVAL_QUERIES.length,
    recall_at_1_baseline: mean(baseline),
    recall_at_1_expanded: mean(expanded),
  };
}
