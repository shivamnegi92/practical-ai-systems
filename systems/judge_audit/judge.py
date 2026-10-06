"""Audit a simple claim-checking judge against two human ratings.

The judge is deliberately transparent and lexical; this example evaluates
agreement mechanics, not the quality of any hosted LLM-as-judge system.
"""
from __future__ import annotations
import re
from common.evaluation import cohen_kappa


def judge(claim: str, evidence: str) -> str:
    claim_terms=set(re.findall(r"[a-z0-9]+",claim.lower()))
    evidence_terms=set(re.findall(r"[a-z0-9]+",evidence.lower()))
    overlap=len(claim_terms & evidence_terms)/len(claim_terms) if claim_terms else 0
    return "supported" if overlap >= 0.5 else "unsupported"


def audit(rows: list[dict]) -> dict:
    predictions=[judge(r['claim'],r['evidence']) for r in rows]
    human_a=[r['human_a'] for r in rows]; human_b=[r['human_b'] for r in rows]
    agreement=sum(a==b for a,b in zip(predictions,human_a))/len(rows) if rows else 0
    return {"cases":len(rows),"judge_human_a_agreement":agreement,"human_interrater_kappa":cohen_kappa(human_a,human_b),"judge_vs_human_kappa":cohen_kappa(predictions,human_a),"warning":"Synthetic labels; a lexical heuristic, not an LLM judge or quality claim."}
