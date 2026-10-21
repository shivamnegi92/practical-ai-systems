// Check whether inline [chunk_id] citations are lexically supported by the cited chunk.
// Flags fabricated or mismatched citations using token overlap. Cannot verify
// numeric facts or anything a cited chunk merely implies.

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

export interface CitationResult {
  chunk_id: string;
  sentence: string;
  overlap: number;
  status: "supported" | "unsupported" | "unknown_chunk";
}

export function checkCitations(answer: string, chunks: Record<string, string>, minOverlap = 0.3) {
  if (typeof minOverlap !== "number" || Number.isNaN(minOverlap) || minOverlap < 0 || minOverlap > 1) {
    throw new RangeError(`minOverlap must be a number between 0 and 1, got ${minOverlap}`);
  }
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
      results.push({ chunk_id: chunkId, sentence: sent, overlap: Math.round(overlap * 10000) / 10000, status });
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
  "billing.md#1": "The Pro plan costs $8 per user per month and removes notebook limits.",
  "sync.md#1": "Notes sync automatically every 60 seconds while you are online.",
};

export interface EvalCase {
  answer: string;
  expectAllSupported: boolean;
}

export const EVAL_CASES: EvalCase[] = [
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
