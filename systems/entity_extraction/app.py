"""Find names, dates, and amounts in business text using explicit patterns."""
import re
def prf(tp: int, fp: int, fn: int) -> dict:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}

PATTERNS = {
    "PERSON": re.compile(r"\b[A-Z][a-z]+\s+[A-Z][a-z]+\b"),
    "DATE": re.compile(r"\b(?:\d{4}-\d{2}-\d{2}|Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:,?\s+\d{4})?\b", re.I),
    "MONEY": re.compile(r"\$\s?\d[\d,]*(?:\.\d{2})?"),
}
PLACES = {"new york", "san francisco", "los angeles", "new delhi"}

def extract(text: str) -> list[dict]:
    entities=[]
    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            kind = "LOCATION" if label == "PERSON" and " ".join(match.group().lower().split()) in PLACES else label
            entities.append({"text":match.group(),"type":kind,"start":match.start(),"end":match.end()})
    return sorted(entities,key=lambda x:(x["start"],x["end"],x["type"]))

def score(predicted: list[dict], gold: list[dict]) -> dict:
    p={(x["text"],x["type"]) for x in predicted}; g={(x["text"],x["type"]) for x in gold}
    return prf(len(p&g),len(p-g),len(g-p))
