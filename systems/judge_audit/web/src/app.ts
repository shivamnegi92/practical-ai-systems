// Audit a simple claim-checking judge against two human ratings.
// The judge is deliberately transparent and lexical; this evaluates
// agreement mechanics, not the quality of any hosted LLM-as-judge system.

export function cohenKappa(a: string[], b: string[]): number {
  if (a.length !== b.length || a.length === 0) throw new Error("raters must label the same non-empty set");
  const n = a.length;
  const observed = a.filter((x, i) => x === b[i]).length / n;
  const countA = new Map<string, number>();
  const countB = new Map<string, number>();
  for (const x of a) countA.set(x, (countA.get(x) ?? 0) + 1);
  for (const x of b) countB.set(x, (countB.get(x) ?? 0) + 1);
  let expected = 0;
  for (const [label, ca] of countA) expected += ca * (countB.get(label) ?? 0);
  expected /= n * n;
  return expected === 1 ? 1 : (observed - expected) / (1 - expected);
}

export function judge(claim: string, evidence: string): "supported" | "unsupported" {
  const claimNumbers = new Set(claim.match(/\b[0-9]+(?:\.[0-9]+)?\b/g) ?? []);
  const evidenceNumbers = new Set(evidence.match(/\b[0-9]+(?:\.[0-9]+)?\b/g) ?? []);
  if ([...claimNumbers].some((number) => !evidenceNumbers.has(number))) return "unsupported";
  const claimTerms = new Set(claim.toLowerCase().match(/[a-z0-9]+/g) ?? []);
  const evidenceTerms = new Set(evidence.toLowerCase().match(/[a-z0-9]+/g) ?? []);
  const overlap = claimTerms.size ? [...claimTerms].filter((t) => evidenceTerms.has(t)).length / claimTerms.size : 0;
  return overlap >= 0.5 ? "supported" : "unsupported";
}

export interface Row {
  claim: string;
  evidence: string;
  human_a: string;
  human_b: string;
}

export function audit(rows: Row[]) {
  const predictions = rows.map((r) => judge(r.claim, r.evidence));
  const humanA = rows.map((r) => r.human_a);
  const humanB = rows.map((r) => r.human_b);
  const agreement = rows.length ? predictions.filter((p, i) => p === humanA[i]).length / rows.length : 0;
  return {
    cases: rows.length,
    judge_human_a_agreement: agreement,
    human_interrater_kappa: cohenKappa(humanA, humanB),
    judge_vs_human_kappa: cohenKappa(predictions, humanA),
    warning: "Synthetic labels; a lexical heuristic, not an LLM judge or quality claim.",
  };
}

export const SAMPLE_ROWS: Row[] = [
  { claim: "The Pro plan costs $8 per month", evidence: "The Pro plan costs $8 per user per month.", human_a: "supported", human_b: "supported" },
  { claim: "Notes sync every 10 minutes", evidence: "Notes sync automatically every 60 seconds.", human_a: "unsupported", human_b: "unsupported" },
  { claim: "Recovery codes work once", evidence: "Each recovery code works only once.", human_a: "supported", human_b: "supported" },
  { claim: "Exports support video", evidence: "Exports are available as Markdown, PDF, or HTML.", human_a: "unsupported", human_b: "supported" },
];

export function evaluateAll() {
  return audit(SAMPLE_ROWS);
}
