"""Audit a simple claim-checking judge against two human ratings.

The judge is deliberately transparent and lexical; this example evaluates
agreement mechanics, not the quality of any hosted LLM-as-judge system.
"""
from __future__ import annotations
import re
from collections import Counter


def cohen_kappa(a: list, b: list) -> float:
    """Agreement between two raters beyond chance."""
    if len(a) != len(b) or not a:
        raise ValueError("raters must label the same non-empty set")
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum(ca[label] * cb[label] for label in ca) / (n * n)
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


def judge(claim: str, evidence: str) -> str:
    claim_terms=set(re.findall(r"[a-z0-9]+",claim.lower()))
    evidence_terms=set(re.findall(r"[a-z0-9]+",evidence.lower()))
    overlap=len(claim_terms & evidence_terms)/len(claim_terms) if claim_terms else 0
    return "supported" if overlap >= 0.5 else "unsupported"


def audit(rows: list[dict]) -> dict:
    if not rows:
        return {"cases":0,"judge_human_a_agreement":0.0,"human_interrater_kappa":0.0,"judge_vs_human_kappa":0.0,"warning":"Synthetic labels; a lexical heuristic, not an LLM judge or quality claim."}
    predictions=[judge(r['claim'],r['evidence']) for r in rows]
    human_a=[r['human_a'] for r in rows]; human_b=[r['human_b'] for r in rows]
    agreement=sum(a==b for a,b in zip(predictions,human_a))/len(rows)
    return {"cases":len(rows),"judge_human_a_agreement":agreement,"human_interrater_kappa":cohen_kappa(human_a,human_b),"judge_vs_human_kappa":cohen_kappa(predictions,human_a),"warning":"Synthetic labels; a lexical heuristic, not an LLM judge or quality claim."}
