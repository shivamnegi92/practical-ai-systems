import unittest
from systems.voice_eval.app import score_turns

class VoiceEvalTests(unittest.TestCase):
 def test_finds_required_and_forbidden_actions(self):
  result=score_turns([{'speaker':'agent','text':'I can help','actions':['issue_refund']}],['appointment moved to Friday'],['issue_refund'])
  self.assertFalse(result['safe']); self.assertFalse(result['task_success'])
 def test_missing_latency_is_unknown(self):
  result=score_turns([],[],[])
  self.assertIsNone(result['median_latency_ms'])
