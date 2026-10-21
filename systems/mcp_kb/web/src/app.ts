// Minimal MCP JSON-RPC tool server logic (tools/list and tools/call),
// adapted for in-browser use instead of stdio. Same dispatch shape as the
// Python stdio server in systems/mcp_kb/server.py.

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

class BM25 {
  tokens: Record<string, string[]> = {};
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

export const CHUNKS: Record<string, string> = {
  "accounts.md#1": 'To reset your password, open the sign-in page, choose "Forgot password", and follow the link sent to your email.',
  "billing.md#1": "The Free plan includes up to 3 notebooks and 500 MB of storage. The Pro plan costs $8 per user per month.",
  "sharing.md#1": "You can share a notebook by email invitation or with a view-only public link.",
  "sync.md#1": "Notes sync automatically every 60 seconds while you are online.",
};

export class KnowledgeTools {
  index = new BM25(CHUNKS);

  search(query: string, limit = 3) {
    const hits = this.index.search(query, Math.max(1, Math.min(limit, 10)));
    return { results: hits.map(([id, score]) => ({ id, text: CHUNKS[id], score: Math.round(score * 10000) / 10000 })) };
  }

  read(chunkId: string) {
    if (!(chunkId in CHUNKS)) throw new Error("unknown chunk id");
    return { id: chunkId, text: CHUNKS[chunkId] };
  }
}

function toolDefinitions() {
  return [
    { name: "search_docs", description: "Search the bundled synthetic docs" },
    { name: "read_chunk", description: "Read one retrieved chunk by id" },
  ];
}

function callTool(params: { name?: string; arguments?: Record<string, unknown> }, tools: KnowledgeTools) {
  const { name, arguments: args = {} } = params;
  try {
    let result: unknown;
    if (name === "search_docs") result = tools.search(args.query as string, args.limit as number | undefined);
    else if (name === "read_chunk") result = tools.read(args.chunk_id as string);
    else throw new Error("unknown tool");
    return { content: [{ type: "text", text: JSON.stringify(result) }] };
  } catch (exc) {
    return { content: [{ type: "text", text: String((exc as Error).message) }], isError: true };
  }
}

export function dispatch(message: { method?: string; params?: Record<string, unknown>; id?: unknown }, tools: KnowledgeTools) {
  if (typeof message !== "object" || message === null || Array.isArray(message) || typeof message.method !== "string") {
    return { jsonrpc: "2.0", id: null, error: { code: -32600, message: "invalid request" } };
  }
  const { method, params = {}, id } = message;
  let result: unknown;
  if (method === "initialize") {
    result = { protocolVersion: "2024-11-05", capabilities: { tools: {} }, serverInfo: { name: "local-knowledge-base", version: "0.1.0" } };
  } else if (method === "notifications/initialized") {
    return {};
  } else if (method === "tools/list") {
    result = { tools: toolDefinitions() };
  } else if (method === "tools/call") {
    result = callTool(params as { name?: string; arguments?: Record<string, unknown> }, tools);
  } else {
    return { jsonrpc: "2.0", id, error: { code: -32601, message: "method not found" } };
  }
  return { jsonrpc: "2.0", id, result };
}

export function evaluateAll() {
  const tools = new KnowledgeTools();
  const queries = [
    { query: "How do I reset my password?", gold: "accounts.md#1" },
    { query: "How much does the Pro plan cost?", gold: "billing.md#1" },
    { query: "How do I share a notebook?", gold: "sharing.md#1" },
    { query: "How often do notes sync?", gold: "sync.md#1" },
  ];
  const hits = queries.map((q) => tools.search(q.query, 3).results.some((r) => r.id === q.gold));
  const recall = hits.filter(Boolean).length / hits.length;
  return { cases: queries.length, recall_at_3: recall };
}
