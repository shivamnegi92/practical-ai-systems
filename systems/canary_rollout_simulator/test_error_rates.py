import unittest
from systems.canary_rollout_simulator.app import decide

class ErrorRateTests(unittest.TestCase):
 def test_invalid_rates_hold_instead_of_supporting_a_decision(self):
  valid={'error_rate':.01,'p95_latency_ms':200}
  for side in ('baseline','canary'):
   for rate in (-.01,1.01,float('nan'),float('inf'),float('-inf'),True,None,'0.1'):
    metrics={'error_rate':rate,'p95_latency_ms':200}
    with self.subTest(side=side,rate=rate):
     result=decide(metrics,valid) if side=='baseline' else decide(valid,metrics)
     self.assertEqual(result['decision'],'hold')
     self.assertEqual(result['reasons'],[f'invalid_{side}_error_rate'])
     self.assertIsNone(result['error_rate_delta'])
     self.assertIsNone(result['latency_regression_pct'])
 def test_both_invalid_sources_and_valid_endpoints(self):
  result=decide({'error_rate':-1,'p95_latency_ms':200},{'error_rate':2,'p95_latency_ms':200})
  self.assertEqual(result['reasons'],['invalid_baseline_error_rate','invalid_canary_error_rate'])
  for rate in (0,1):
   metrics={'error_rate':rate,'p95_latency_ms':200}
   self.assertEqual(decide(metrics,metrics)['decision'],'promote')
  self.assertEqual(decide({'error_rate':0,'p95_latency_ms':200},{'error_rate':1,'p95_latency_ms':200})['decision'],'rollback')
