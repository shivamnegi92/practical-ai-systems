import json
from pathlib import Path
from systems.semantic_cache.cache import SemanticCache

def evaluate():
 rows=json.loads((Path(__file__).parent/'eval'/'cases.json').read_text()); cache=SemanticCache()
 for row in rows: cache.put(row['query'],row['response'])
 for row in rows: assert cache.get(row['query'])==row['response']
 lookups=[row for row in rows if 'lookup' in row]
 for row in lookups:
  expected=row['response'] if row['should_hit'] else None
  assert cache.get(row['lookup'])==expected
 return {'entries':len(rows),'exact_replay_rate':1.0,'normalized_lookup_accuracy':1.0,'normalized_lookup_cases':len(lookups),'estimated_call_reduction_on_repeated_identical_workload':0.5,'note':'Synthetic replay and punctuation lookup cases only; illustrative two-pass exact-key workload, not production savings. No paraphrase matching; punctuation normalization can conflate meaning.'}
if __name__=='__main__': print(json.dumps(evaluate(),indent=2))
