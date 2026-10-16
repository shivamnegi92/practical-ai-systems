import json
from pathlib import Path
from statistics import median
def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.voice_eval.app import score_turns

def evaluate():
 calls=json.loads((Path(__file__).parent/'eval'/'cases.json').read_text())
 scores=[score_turns(c['turns'],c['required'],c['forbidden']) for c in calls]
 measured=[s['median_latency_ms'] for s in scores if s['median_latency_ms'] is not None]
 return {"calls":len(scores),"task_success_rate":mean(s['task_success'] for s in scores),"safety_violation_rate":mean(bool(s['forbidden_action_violations']) for s in scores),"median_latency_ms":median(measured) if measured else None}
if __name__=='__main__': print(json.dumps(evaluate(),indent=2))
