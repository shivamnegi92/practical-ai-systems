import unittest
from systems.voice_eval.app import score_turns

class VoiceEvalTests(unittest.TestCase):
 def test_finds_required_and_forbidden_actions(self):
  result=score_turns([{'speaker':'agent','text':'I can help','actions':['issue_refund']}],['appointment moved to Friday'],['issue_refund'])
  self.assertFalse(result['safe']); self.assertFalse(result['task_success'])
 def test_missing_latency_is_unknown(self):
  result=score_turns([],[],[])
  self.assertIsNone(result['median_latency_ms'])
 def test_terms_in_different_sentences_do_not_satisfy_requirement(self):
  turns=[{'speaker':'agent','text':'Your appointment is still on Monday. Have a good Friday.'}]
  result=score_turns(turns,['appointment moved to Friday'])
  self.assertFalse(result['task_success'])
  self.assertEqual(result['missing_requirements'],['appointment moved to Friday'])
