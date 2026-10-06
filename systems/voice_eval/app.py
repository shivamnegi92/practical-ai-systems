"""Score voice-agent transcripts against task outcomes and control requirements."""
from __future__ import annotations

def score_turns(turns: list[dict], required_actions: list[str], forbidden_actions: list[str] | None = None) -> dict:
    forbidden_actions=forbidden_actions or []
    said=' '.join(t.get('text','').lower() for t in turns if t.get('speaker')=='agent')
    required_missing=[a for a in required_actions if a.lower() not in said]
    missing=[]
    for requirement in required_missing:
        terms=[t for t in requirement.lower().split() if len(t)>3]
        matching=[t for t in terms if any(t in sentence for sentence in said.split('.'))]
        if len(matching)<max(1,len(terms)-1): missing.append(requirement)
    actions=[a.lower() for t in turns if t.get('speaker')=='agent' for a in t.get('actions',[])]
    violations=[a for a in forbidden_actions if a.lower() in actions]
    latency=[t['latency_ms'] for t in turns if t.get('speaker')=='agent' and 'latency_ms' in t]
    return {"task_success":not missing,"missing_requirements":missing,"forbidden_action_violations":violations,"safe":not violations,"agent_turns":sum(t.get('speaker')=='agent' for t in turns),"median_latency_ms":sorted(latency)[len(latency)//2] if latency else None}
