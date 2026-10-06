import json
from pathlib import Path
from common.evaluation import mean
from systems.entity_extraction.app import extract, score


def evaluate():
    cases=json.loads((Path(__file__).parent/'eval'/'cases.json').read_text())
    scores=[score(extract(c['text']),c['gold']) for c in cases]
    return {"cases":len(cases),"micro_like_average_precision":round(mean(s['precision'] for s in scores),4),"micro_like_average_recall":round(mean(s['recall'] for s in scores),4),"micro_like_average_f1":round(mean(s['f1'] for s in scores),4),"note":"Macro average across cases; small synthetic set."}

if __name__ == '__main__': print(json.dumps(evaluate(),indent=2))
