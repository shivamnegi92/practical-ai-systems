import unittest

from systems.trace_anomaly_detector.app import detect_anomalies

BASELINE = [95, 100, 105, 98, 102, 97, 103, 99, 101, 100]


class TraceAnomalyDetectorTests(unittest.TestCase):
    def test_flat_baseline_flags_spike_beyond_strict_relative_tolerance(self):
        durations = [10000, 100, 150, 151, 50, 49]
        result = detect_anomalies([100, 100, 100], [{'name':str(d), 'duration_ms':d} for d in durations])
        self.assertEqual([row['anomalous'] for row in result], [True, False, False, True, False, True])

    def test_zero_mean_and_missing_baseline_are_distinct(self):
        traces = [{'name':'same','duration_ms':0}, {'name':'spike','duration_ms':1}]
        self.assertEqual([r['anomalous'] for r in detect_anomalies([0,0], traces)], [False, True])
        self.assertEqual([r['anomalous'] for r in detect_anomalies([], traces)], [False, False])
        self.assertTrue(detect_anomalies([], [{'name':'error','duration_ms':0,'error':True}])[0]['anomalous'])
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


if __name__ == "__main__":
    unittest.main()
