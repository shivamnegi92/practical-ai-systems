import unittest

from systems.canary_rollout_simulator.app import decide

BASELINE = {"error_rate": 0.01, "p95_latency_ms": 200}


class CanaryRolloutSimulatorTests(unittest.TestCase):
    def test_zero_or_missing_latency_baseline_holds(self):
        for baseline in ({'error_rate':0,'p95_latency_ms':0}, {'error_rate':0}):
            for duration in (0, 9999):
                with self.subTest(baseline=baseline, duration=duration):
                    result=decide(baseline, {'error_rate':0,'p95_latency_ms':duration})
                    self.assertEqual(result['decision'],'hold')
                    self.assertIn('missing_latency_baseline',result['reasons'])
                    self.assertIsNone(result['latency_regression_pct'])

    def test_known_error_regression_still_rolls_back_without_latency_baseline(self):
        result=decide({'error_rate':0,'p95_latency_ms':0},{'error_rate':0.05,'p95_latency_ms':9999})
        self.assertEqual(result['decision'],'rollback')
        self.assertIn('error_rate_regression',result['reasons'])
    def test_promotes_when_within_guardrails(self):
        canary = {"error_rate": 0.015, "p95_latency_ms": 210}
        self.assertEqual(decide(BASELINE, canary)["decision"], "promote")

    def test_rolls_back_on_error_rate_spike(self):
        canary = {"error_rate": 0.05, "p95_latency_ms": 205}
        result = decide(BASELINE, canary)
        self.assertEqual(result["decision"], "rollback")
        self.assertIn("error_rate_regression", result["reasons"])

    def test_rolls_back_on_latency_regression(self):
        canary = {"error_rate": 0.012, "p95_latency_ms": 400}
        result = decide(BASELINE, canary)
        self.assertEqual(result["decision"], "rollback")
        self.assertIn("latency_regression", result["reasons"])


if __name__ == "__main__":
    unittest.main()
