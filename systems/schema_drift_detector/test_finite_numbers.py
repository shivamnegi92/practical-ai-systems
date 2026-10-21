import unittest
from systems.schema_drift_detector.app import detect_drift
class FiniteNumbers(unittest.TestCase):
 def test_nonfinite_observations_report_numeric_drift(self):
  for value in (float("nan"),float("inf"),float("-inf")):
   with self.subTest(value=value):
    result=detect_drift({"amount":{"type":"number"}},[{"amount":value}])
    self.assertTrue(result["drift_detected"])
    self.assertEqual(result["type_mismatched_fields"],["amount"])
 def test_finite_numbers_and_optional_null_are_unchanged(self):
  for value in (0,-1,2.5,None,10**1000):
   with self.subTest(value=type(value).__name__):self.assertFalse(detect_drift({"amount":{"type":"number"}},[{"amount":value}])["drift_detected"])
 def test_boolean_still_is_not_a_number(self):
  self.assertTrue(detect_drift({"amount":{"type":"number"}},[{"amount":True}])["drift_detected"])
