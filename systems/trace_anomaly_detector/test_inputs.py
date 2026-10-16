import unittest
from systems.trace_anomaly_detector.app import detect_anomalies

class TraceInputTests(unittest.TestCase):
 def test_invalid_baseline_durations_thresholds_are_rejected(self):
  for value in (-1,float('nan'),float('inf'),float('-inf'),True,None,'1',10**400):
   with self.subTest(value=value):
    with self.assertRaisesRegex(ValueError,'baseline'):detect_anomalies([10,value],[])
    with self.assertRaisesRegex(ValueError,'duration'):detect_anomalies([10,20],[{'name':'bad','duration_ms':value}])
    with self.assertRaisesRegex(ValueError,'threshold'):detect_anomalies([],[],value)
 def test_valid_zero_fractional_and_error_flag_controls(self):
  result=detect_anomalies([10,20],[{'name':'normal','duration_ms':15},{'name':'flagged','duration_ms':15,'error':True}],.5)
  self.assertFalse(result[0]['anomalous']);self.assertTrue(result[1]['anomalous'])
  self.assertEqual(detect_anomalies([],[],0),[])
  self.assertEqual(detect_anomalies([0,1],[{'name':'zero','duration_ms':0}],0)[0]['name'],'zero')
