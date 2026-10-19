import unittest

from systems.trace_anomaly_detector.app import detect_anomalies

BASELINE = [95, 100, 105, 98, 102, 97, 103, 99, 101, 100]


class TraceAnomalyDetectorTests(unittest.TestCase):
    def test_duration_near_baseline_is_not_anomalous(self):
        results = detect_anomalies(BASELINE, [{"name": "normal", "duration_ms": 101}])
        self.assertFalse(results[0]["anomalous"])

    def test_large_spike_is_anomalous(self):
        results = detect_anomalies(BASELINE, [{"name": "spike", "duration_ms": 500}])
        self.assertTrue(results[0]["anomalous"])

    def test_error_flag_forces_anomalous_regardless_of_duration(self):
        results = detect_anomalies(BASELINE, [{"name": "error_but_fast", "duration_ms": 100, "error": True}])
        self.assertTrue(results[0]["anomalous"])

    def test_zero_variance_baseline_does_not_crash(self):
        results = detect_anomalies([100, 100, 100], [{"name": "flat", "duration_ms": 500}])
        self.assertEqual(results[0]["z_score"], 0.0)

    def test_invalid_z_threshold_raises_value_error(self):
        for invalid in [0, -1.5, "3.0", True, float("nan")]:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    detect_anomalies(BASELINE, [{"name": "sample", "duration_ms": 100}], z_threshold=invalid)


if __name__ == "__main__":
    unittest.main()
