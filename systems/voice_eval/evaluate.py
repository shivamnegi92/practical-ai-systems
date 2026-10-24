"""Score a shared synthetic transcript matrix against explicit gold labels."""
import json
from pathlib import Path
from systems.voice_eval.app import score_turns

def mean(values):
    values=list(values)
    return sum(values)/len(values) if values else 0.0

def evaluate():
    calls=json.loads((Path(__file__).parent/'eval'/'cases.json').read_text())
    scores=[score_turns(c['turns'],c['required'],c['forbidden']) for c in calls]
    latencies=sorted(s['median_latency_ms'] for s in scores if s['median_latency_ms'] is not None)
    return {
        "calls":len(scores),
        "task_success_rate":mean(s['task_success'] for s in scores),
        "safety_violation_rate":mean(bool(s['forbidden_action_violations']) for s in scores),
        "median_latency_ms":latencies[len(latencies)//2] if latencies else None,
        "task_success_accuracy":mean(s['task_success']==c['gold_task_success'] for s,c in zip(scores,calls)),
        "safety_accuracy":mean(s['safe']==c['gold_safe'] for s,c in zip(scores,calls)),
    }

if __name__=='__main__': print(json.dumps(evaluate(),indent=2))
