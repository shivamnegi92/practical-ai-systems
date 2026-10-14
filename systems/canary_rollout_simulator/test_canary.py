import unittest

from systems.canary_rollout_simulator.app import decide

BASELINE = {"error_rate": 0.01, "p95_latency_ms": 200}


class CanaryRolloutSimulatorTests(unittest.TestCase):
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


class EvaluationCoverage(unittest.TestCase):
    def test_invalid_rate_labels_remain_visible(self):
        from systems.canary_rollout_simulator.evaluate import evaluate
        result = evaluate()
        self.assertEqual(result["cases"], 12)
        self.assertEqual(result["decision_accuracy"], 0.8333)
