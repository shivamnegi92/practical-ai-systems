import json
from pathlib import Path
from common.evaluation import mean
from systems.bounded_agent.app import BoundedAgent

def evaluate():
 cases=json.loads((Path(__file__).parent/'eval'/'cases.json').read_text()); agent=BoundedAgent({'lookup_order':lambda order_id:{'order_id':order_id},'send_refund':lambda amount:{'queued':amount}}, {'lookup_order','send_refund'}, approval_required={'send_refund'})
 results=[]
 for c in cases:
  try: result=agent.run(agent.plan(c['request']),c['approved'])['status']
  except ValueError: result='rejected'
  results.append(result==c['expected'])
 return {'cases':len(cases),'policy_cases_passed':sum(results),'policy_accuracy':mean(results)}
if __name__=='__main__': print(json.dumps(evaluate(),indent=2))
