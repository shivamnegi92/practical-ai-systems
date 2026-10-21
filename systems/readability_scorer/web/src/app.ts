// Approximate Flesch-Kincaid reading grade level using a vowel-run syllable heuristic.

export function sentences(text: string): string[] {
  return text.trim().split(/(?<=[.!?])\s+/).map((s) => s.trim()).filter(Boolean);
}

function syllables(word: string): number {
  const w = word.toLowerCase();
  let count = (w.match(/[aeiouy]+/g) ?? []).length;
  if (w.endsWith("e") && count > 1) count -= 1;
  return Math.max(count, 1);
}

export function gradeLevel(text: string): number {
  const words = text.match(/[A-Za-z]+(?:['\u2019][A-Za-z]+)*/g) ?? [];
  const sents = sentences(text).length ? sentences(text) : [text];
  if (words.length === 0) return 0;
  const totalSyllables = words.reduce((sum, w) => sum + syllables(w), 0);
  const score = 0.39 * (words.length / sents.length) + 11.8 * (totalSyllables / words.length) - 15.59;
  return Math.round(score * 100) / 100;
}

export function band(grade: number): "simple" | "standard" | "complex" {
  if (grade <= 6) return "simple";
  if (grade <= 12) return "standard";
  return "complex";
}

export interface EvalCase {
  text: string;
  band: string;
}

export const EVAL_CASES: EvalCase[] = [
  { text: "The cat sat on the mat. It was a hot day.", band: "simple" },
  { text: "I like dogs. Dogs are fun. We play all day.", band: "simple" },
  { text: "Our new feature lets you schedule reports automatically every week.", band: "standard" },
  {
    text: "Notwithstanding the aforementioned stipulations, the organization's multifaceted obligations necessitate comprehensive reevaluation.",
    band: "complex",
  },
];

export function evaluateAll() {
  const correct = EVAL_CASES.filter((c) => band(gradeLevel(c.text)) === c.band).length;
  return { cases: EVAL_CASES.length, band_accuracy: correct / EVAL_CASES.length };
}
