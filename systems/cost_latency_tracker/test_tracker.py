import unittest

from systems.cost_latency_tracker.app import check_budget, summarize


class CostLatencyTrackerTests(unittest.TestCase):
    def test_summarize_computes_percentiles_and_cost(self):
        requests = [{"latency_ms": 100, "cost_usd": 0.01, "tokens": 1000} for _ in range(5)]
        summary = summarize(requests)
        self.assertEqual(summary["requests"], 5)
        self.assertEqual(summary["p50_latency_ms"], 100)
        self.assertAlmostEqual(summary["total_cost_usd"], 0.05)

    def test_budget_breach_on_latency(self):
        summary = {"p95_latency_ms": 500, "total_cost_usd": 0.1}
        decision = check_budget(summary, max_p95_latency_ms=300, max_cost_usd=1.0)
        self.assertTrue(decision["breached"])
        self.assertIn("latency", decision["reasons"])

    def test_no_breach_within_budget(self):
        summary = {"p95_latency_ms": 100, "total_cost_usd": 0.5}
        decision = check_budget(summary, max_p95_latency_ms=300, max_cost_usd=1.0)
        self.assertFalse(decision["breached"])

    def test_zero_tokens_gives_zero_cost_rate(self):
        summary = summarize([{"latency_ms": 10, "cost_usd": 0.0, "tokens": 0}])
        self.assertEqual(summary["cost_per_1k_tokens_usd"], 0.0)


if __name__ == "__main__":
    unittest.main()


class EvaluationCoverage(unittest.TestCase):
    def test_expanded_budget_matrix(self):
        from systems.cost_latency_tracker.evaluate import evaluate
        result = evaluate()
        self.assertEqual(result["cases"], 10)
        self.assertEqual(result["breach_decision_accuracy"], 0.8)
