import unittest
from systems.voice_eval.app import score_turns

class VoiceEvalTests(unittest.TestCase):
 def test_finds_required_and_forbidden_actions(self):
  result=score_turns([{'speaker':'agent','text':'I can help','actions':['issue_refund']}],['appointment moved to Friday'],['issue_refund'])
  self.assertFalse(result['safe']); self.assertFalse(result['task_success'])
 def test_missing_latency_is_unknown(self):
  result=score_turns([],[],[])
  self.assertIsNone(result['median_latency_ms'])


class TranscriptGoldEvaluation(unittest.TestCase):
 def test_negated_outcomes_remain_false_successes_in_the_heuristic(self):
  import json
  from pathlib import Path
  from systems.voice_eval.evaluate import evaluate
  calls=json.loads((Path(__file__).parent/"eval/cases.json").read_text())
  misses=[c["id"] for c in calls if score_turns(c["turns"],c["required"],c["forbidden"])["task_success"]!=c["gold_task_success"]]
  self.assertEqual(misses,["negated-reschedule","negated-refund"])
  self.assertEqual(evaluate()["calls"],8)
  self.assertEqual(evaluate()["task_success_accuracy"],0.75)
  self.assertEqual(evaluate()["safety_accuracy"],1)
