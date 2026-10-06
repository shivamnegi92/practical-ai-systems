import unittest
from systems.judge_audit.judge import audit, judge

class JudgeTests(unittest.TestCase):
 def test_detects_explicit_evidence_overlap(self):
  self.assertEqual(judge('Pro costs eight dollars','Pro costs $8 monthly'),'supported')
 def test_reports_human_disagreement_not_hidden(self):
  report=audit([{'claim':'a','evidence':'a','human_a':'supported','human_b':'unsupported'}])
  self.assertEqual(report['human_interrater_kappa'],0.0)
  self.assertIn('Synthetic',report['warning'])
