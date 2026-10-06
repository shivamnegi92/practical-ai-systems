"""Find names, dates, and amounts in business text using explicit patterns."""
import re
from common.evaluation import prf

PATTERNS = {
    "PERSON": re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b"),
    "DATE": re.compile(r"\b(?:\d{4}-\d{2}-\d{2}|Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:,?\s+\d{4})?\b", re.I),
    "MONEY": re.compile(r"\$\s?\d[\d,]*(?:\.\d{2})?"),
}

def extract(text: str) -> list[dict]:
    entities=[]
    for label, pattern in PATTERNS.items():
        entities.extend({"text":m.group(),"type":label,"start":m.start(),"end":m.end()} for m in pattern.finditer(text))
    return sorted(entities,key=lambda x:(x["start"],x["end"],x["type"]))

def score(predicted: list[dict], gold: list[dict]) -> dict:
    p={(x["text"],x["type"]) for x in predicted}; g={(x["text"],x["type"]) for x in gold}
    return prf(len(p&g),len(p-g),len(g-p))
