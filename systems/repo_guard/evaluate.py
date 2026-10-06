import json
from pathlib import Path
from systems.repo_guard.app import SECRET_PATTERNS,DANGEROUS_ACTIONS

def evaluate():
 rows=json.loads((Path(__file__).parent/'eval'/'cases.json').read_text()); tp=fp=fn=0
 for row in rows:
  text=row['text']; found=any(p.search(text) for _,p in SECRET_PATTERNS) or bool(DANGEROUS_ACTIONS.search(text)); expected=row['findings']>0
  tp+=found and expected; fp+=found and not expected; fn+=not found and expected
 return {'cases':len(rows),'recall':tp/(tp+fn) if tp+fn else 0,'precision':tp/(tp+fp) if tp+fp else 0,'scope':'toy patterns only; not a security scanner'}
if __name__=='__main__': print(json.dumps(evaluate(),indent=2))
