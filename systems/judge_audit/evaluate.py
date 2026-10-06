import json
from pathlib import Path
from systems.judge_audit.judge import audit

def evaluate(): return audit(json.loads((Path(__file__).parent/'eval'/'cases.json').read_text()))
if __name__=='__main__': print(json.dumps(evaluate(),indent=2))
