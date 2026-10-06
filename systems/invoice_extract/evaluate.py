import json
from pathlib import Path
from systems.invoice_extract.app import extract

CASES = Path(__file__).parent / "eval" / "cases.json"

def evaluate():
    cases=json.loads(CASES.read_text()); total=correct=0; valid_tp=valid_fp=valid_fn=0
    for case in cases:
        got=extract(case["text"])
        for key, expected in case["fields"].items():
            total += 1; correct += getattr(got,key) == expected
        predicted=not got.errors; expected=case["valid"]
        valid_tp += predicted and expected; valid_fp += predicted and not expected; valid_fn += not predicted and expected
    return {"cases":len(cases),"field_exact_match":round(correct/total,4),"validity_precision":round(valid_tp/(valid_tp+valid_fp) if valid_tp+valid_fp else 0,4),"validity_recall":round(valid_tp/(valid_tp+valid_fn) if valid_tp+valid_fn else 0,4)}

if __name__ == "__main__": print(json.dumps(evaluate(),indent=2))
