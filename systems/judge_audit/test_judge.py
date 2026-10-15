import unittest
from systems.judge_audit.judge import audit, judge

class JudgeTests(unittest.TestCase):
 def test_detects_explicit_evidence_overlap(self):
  self.assertEqual(judge('Pro costs eight dollars','Pro costs $8 monthly'),'supported')
 def test_reports_human_disagreement_not_hidden(self):
  report=audit([{'claim':'a','evidence':'a','human_a':'supported','human_b':'unsupported'}])
  self.assertEqual(report['human_interrater_kappa'],0.0)
  self.assertIn('Synthetic',report['warning'])


class EvaluationFailureModes(unittest.TestCase):
 def test_numeric_and_negation_conflicts_remain_visible(self):
  from systems.judge_audit.evaluate import evaluate
  for claim,evidence in [("Pro costs $80 per user per month","Pro costs $8 per user per month."),("Public links can be disabled","Public links cannot be disabled."),("SMS codes are supported","SMS codes are not supported.")]:
   self.assertEqual(judge(claim,evidence),"supported")
  self.assertEqual(evaluate()["cases"],14)
  self.assertLess(evaluate()["judge_human_a_agreement"],1)
