import unittest
from systems.canary_rollout_simulator.app import decide


class ThresholdConfigTests(unittest.TestCase):
    def test_invalid_thresholds_do_not_silently_disable_a_guard(self):
        for value in (-1, float('nan'), float('inf'), True, '0.2', None):
            for field in ('max_error_rate_delta', 'max_latency_regression_pct'):
                with self.subTest(value=value, field=field), self.assertRaises(ValueError):
                    decide({'error_rate': .01, 'p95_latency_ms': 100}, {'error_rate': .5, 'p95_latency_ms': 1000}, **{field: value})

    def test_zero_limits_and_explicit_relaxed_limits(self):
        baseline = {'error_rate': .01, 'p95_latency_ms': 100}
        self.assertEqual(decide(baseline, baseline, 0, 0)['decision'], 'promote')
        self.assertEqual(decide(baseline, {'error_rate': .02, 'p95_latency_ms': 101}, 0, 0)['decision'], 'rollback')
        self.assertEqual(decide(baseline, {'error_rate': .5, 'p95_latency_ms': 1000}, 1, 10)['decision'], 'promote')
