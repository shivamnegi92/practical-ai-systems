// Compute recall@k, MRR, and nDCG@k for ranked retrieval, and compare two strategies.
// Carries its own bundled BM25 index and synonym-expansion query rewriter.

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
  price: ["cost"], pricing: ["cost"], terminate: ["cancel"], unsubscribe: ["cancel"], erase: ["delete"], remove: ["delete"],
};

export function expandQuery(query: string): string {
  const normalized = new Map(Object.entries(SYNONYMS).flatMap(([word, aliases]) => tokenize(word).map(t => [t, aliases] as const)));
  const extra = tokenize(query).flatMap((t) => normalized.get(t) ?? []);
  return [query, ...extra].join(" ");
}

export function recallAtK(rankedIds: string[], relevantIds: Set<string>, k: number): number {
  if (relevantIds.size === 0) return 0;
  const top = new Set(rankedIds.slice(0, k));
  return [...top].filter((id) => relevantIds.has(id)).length / relevantIds.size;
}

export function reciprocalRank(rankedIds: string[], relevantIds: Set<string>): number {
  for (let i = 0; i < rankedIds.length; i++) if (relevantIds.has(rankedIds[i])) return 1 / (i + 1);
  return 0;
}

export function ndcgAtK(rankedIds: string[], relevance: Record<string, number>, k: number): number {
  const dcg = rankedIds.slice(0, k).reduce((sum, id, i) => sum + (relevance[id] ?? 0) / Math.log2(i + 2), 0);
  const ideal = Object.values(relevance).sort((a, b) => b - a).slice(0, k);
  const idcg = ideal.reduce((sum, rel, i) => sum + rel / Math.log2(i + 2), 0);
  return idcg ? dcg / idcg : 0;
}

export function evaluateRanking(rankedIds: string[], relevance: Record<string, number>, k = 3) {
  const relevantIds = new Set(Object.entries(relevance).filter(([, r]) => r > 0).map(([id]) => id));
  return {
    recall_at_k: Math.round(recallAtK(rankedIds, relevantIds, k) * 10000) / 10000,
    mrr: Math.round(reciprocalRank(rankedIds, relevantIds) * 10000) / 10000,
    ndcg_at_k: Math.round(ndcgAtK(rankedIds, relevance, k) * 10000) / 10000,
  };
}

export interface Query { text: string; relevance: Record<string, number> }

export function compareStrategies(corpus: Record<string, string>, queries: Query[], k = 3) {
  const index = new BM25(corpus);
  const baselineScores: ReturnType<typeof evaluateRanking>[] = [];
  const expandedScores: ReturnType<typeof evaluateRanking>[] = [];
  for (const query of queries) {
    const baselineRanked = index.search(query.text, k).map(([id]) => id);
    const expandedRanked = index.search(expandQuery(query.text), k).map(([id]) => id);
    baselineScores.push(evaluateRanking(baselineRanked, query.relevance, k));
    expandedScores.push(evaluateRanking(expandedRanked, query.relevance, k));
  }
  const avg = (metric: "recall_at_k" | "mrr" | "ndcg_at_k", scores: ReturnType<typeof evaluateRanking>[]) =>
    scores.length ? Math.round((scores.reduce((sum, s) => sum + s[metric], 0) / scores.length) * 10000) / 10000 : 0;
  const metrics = ["recall_at_k", "mrr", "ndcg_at_k"] as const;
  return {
    baseline: Object.fromEntries(metrics.map((m) => [m, avg(m, baselineScores)])),
    expanded: Object.fromEntries(metrics.map((m) => [m, avg(m, expandedScores)])),
  };
}

export const CORPUS: Record<string, string> = {
  d1: "Costs are eight dollars monthly.",
  d2: "We ship worldwide within five days.",
  d3: "Cancel requests take one business day.",
  d4: "Delete your account from the settings page.",
};

export const QUERIES: Query[] = [
  { text: "What is the price?", relevance: { d1: 1 } },
  { text: "How do I terminate my account?", relevance: { d3: 1 } },
  { text: "How can I erase my data?", relevance: { d4: 1 } },
];

export function evaluateAll() {
  return compareStrategies(CORPUS, QUERIES);
}
