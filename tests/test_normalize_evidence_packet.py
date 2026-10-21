import unittest
from scripts.evaluate_systems import normalize

class NormalizeEvidencePacket(unittest.TestCase):
 def test_standard_packet_does_not_need_a_duplicate_top_level_count(self):
  result=normalize("demo",{"dataset":{"cases":3},"metrics":{"accuracy":0.5},"method":"offline"})
  self.assertEqual(result["dataset"]["cases"],3)
  self.assertEqual(result["metrics"],{"accuracy":0.5})
 def test_nested_count_keeps_precedence_for_explicit_metrics(self):
  result=normalize("demo",{"calls":2,"dataset":{"cases":3},"metrics":{"accuracy":0.5}})
  self.assertEqual(result["dataset"]["cases"],3)
 def test_flat_evaluator_output_still_works(self):
  result=normalize("demo",{"cases":2,"accuracy":0.5})
  self.assertEqual(result["dataset"]["cases"],2)
 def test_absent_workload_is_still_refused(self):
  with self.assertRaises(ValueError):normalize("demo",{"metrics":{"accuracy":0.5}})
