import unittest
from systems.cost_latency_tracker.app import check_budget, summarize


class MeasurementTests(unittest.TestCase):
    def test_invalid_request_values_are_rejected(self):
        for field in ("latency_ms", "cost_usd", "tokens"):
            values = [-1, float("nan"), float("inf"), -float("inf"), True, "10", None]
            if field == "tokens":
                values += [1.5]
            for value in values:
                row = {"latency_ms": 10, "cost_usd": .01, "tokens": 100}
                row[field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    summarize([row])

    def test_invalid_budget_inputs_never_return_a_clean_verdict(self):
        for field in ("p95_latency_ms", "total_cost_usd", "max_p95", "max_cost"):
            for value in (-1, float("nan"), float("inf"), True, "10", None):
                data = {"p95_latency_ms": 10, "total_cost_usd": .01, "max_p95": 100, "max_cost": 1}
                data[field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    check_budget(data, data["max_p95"], data["max_cost"])

    def test_empty_zero_and_missing_token_inputs_are_valid(self):
        self.assertEqual(summarize([])["total_cost_usd"], 0)
        self.assertEqual(summarize([{"latency_ms": 0, "cost_usd": 0}])["cost_per_1k_tokens_usd"], 0)
        self.assertFalse(check_budget(summarize([]), 0, 0)["breached"])

    def test_aggregate_overflow_is_rejected(self):
        for rows in ([{"latency_ms": 1, "cost_usd": 1e308}] * 2,
                     [{"latency_ms": 1, "cost_usd": 1e308, "tokens": 1}]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                summarize(rows)
