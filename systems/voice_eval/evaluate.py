import json
from pathlib import Path
from common.evaluation import mean
from systems.voice_eval.app import score_turns

def evaluate():
 calls=json.loads((Path(__file__).parent/'eval'/'calls.json').read_text())
 scores=[score_turns(c['turns'],c['required'],c['forbidden']) for c in calls]
 return {"calls":len(scores),"task_success_rate":mean(s['task_success'] for s in scores),"safety_violation_rate":mean(bool(s['forbidden_action_violations']) for s in scores),"median_latency_ms":sorted(s['median_latency_ms'] for s in scores if s['median_latency_ms'] is not None)[len(scores)//2]}
if __name__=='__main__': print(json.dumps(evaluate(),indent=2))
