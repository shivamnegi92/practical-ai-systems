// Check whether inline [chunk_id] citations are lexically supported by the cited chunk.
// Uses lexical overlap plus literal numeric-token presence, not semantic entailment.

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

const CITATION = /\[([^\]]+)\]/g;
const NUMBER = /(?<!\w)[$€£]?[+-]?\d+(?:[.,:/-]\d+)*(?:\s*%)?/g;

function numberTokens(text: string): Set<string> {
  return new Set([...text.matchAll(NUMBER)].map((match)=>match[0].replace(/\s+/g,"")));
}

export interface CitationResult {
  chunk_id: string;
  sentence: string;
  overlap: number;
  status: "supported" | "unsupported" | "unknown_chunk";
  reason?: "number_mismatch";
}

export function checkCitations(answer: string, chunks: Record<string, string>, minOverlap = 0.3) {
  const results: CitationResult[] = [];
  for (const sent of sentences(answer)) {
    const re = new RegExp(CITATION.source, CITATION.flags);
    let match: RegExpExecArray | null;
    while ((match = re.exec(sent)) !== null) {
      const chunkId = match[1];
      if (!(chunkId in chunks)) {
        results.push({ chunk_id: chunkId, sentence: sent, overlap: 0, status: "unknown_chunk" });
        continue;
      }
      const claimTokens = new Set(tokenize(sent));
      const chunkTokens = new Set(tokenize(chunks[chunkId]));
      const overlap = claimTokens.size
        ? [...claimTokens].filter((t) => chunkTokens.has(t)).length / claimTokens.size
        : 0;
      const status = overlap >= minOverlap ? "supported" : "unsupported";
      const sourceNumbers=numberTokens(chunks[chunkId]);
      const mismatch=[...numberTokens(sent.replace(CITATION,""))].some((token)=>!sourceNumbers.has(token));
      const row: CitationResult = { chunk_id: chunkId, sentence: sent, overlap: Math.round(overlap * 10000) / 10000, status: mismatch ? "unsupported" : status };
      if (mismatch) row.reason="number_mismatch";
      results.push(row);
    }
  }
  return {
    citations: results.length,
    results,
    unsupported: results.filter((r) => r.status !== "supported"),
    all_supported: results.length ? results.every((r) => r.status === "supported") : true,
  };
}

export const SAMPLE_CHUNKS: Record<string, string> = {
  "schedule.md#1": "The deadline is 2026-01-01.",
  "rates.md#1": "The discount rate is 2%.",
  "billing.md#1": "The Pro plan costs $8 per user per month and removes notebook limits.",
  "sync.md#1": "Notes sync automatically every 60 seconds while you are online.",
};

export interface EvalCase {
  answer: string;
  expectAllSupported: boolean;
}

export const EVAL_CASES: EvalCase[] = [
  { answer: "The Pro plan costs $80 per user per month [billing.md#1].", expectAllSupported: false },
  { answer: "The deadline is 2026-01-02 [schedule.md#1].", expectAllSupported: false },
  { answer: "The discount rate is 20% [rates.md#1].", expectAllSupported: false },
  { answer: "The deadline is 2026-01-01 [schedule.md#1].", expectAllSupported: true },
  { answer: "The Pro plan costs $8 per month [billing.md#1].", expectAllSupported: true },
  { answer: "Notes sync every 60 seconds [sync.md#1].", expectAllSupported: true },
  { answer: "The Pro plan includes unlimited video calls [billing.md#1].", expectAllSupported: false },
  { answer: "This is backed by data [made-up.md#9].", expectAllSupported: false },
];

export function evaluateAll() {
  const correct = EVAL_CASES.filter(
    (c) => checkCitations(c.answer, SAMPLE_CHUNKS).all_supported === c.expectAllSupported
  ).length;
  return { cases: EVAL_CASES.length, accuracy: correct / EVAL_CASES.length };
}
