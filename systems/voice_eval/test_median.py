import json
import unittest
from unittest.mock import patch
from systems.voice_eval.app import score_turns
from systems.voice_eval.evaluate import evaluate

class MedianTests(unittest.TestCase):
    def test_even_and_odd_agent_latencies(self):
        for values, expected in [([650, 420], 535), ([30, 10, 20], 20), ([7], 7), ([0, 1], .5), ([], None)]:
            with self.subTest(values=values):
                turns = [{"speaker": "caller", "latency_ms": 99999}]
                turns += [{"speaker": "agent", "latency_ms": x} for x in values]
                turns.append({"speaker": "agent"})
                self.assertEqual(score_turns(turns, [])["median_latency_ms"], expected)

    def test_evaluator_uses_only_measured_calls(self):
        for values, expected in [([10, 30, None], 20), ([None], None), ([], None)]:
            calls = [{"required": [], "forbidden": [], "turns": [{"speaker": "agent", **({"latency_ms": n} if n is not None else {})}]} for n in values]
            with self.subTest(values=values), patch("pathlib.Path.read_text", return_value=json.dumps(calls)):
                self.assertEqual(evaluate()["median_latency_ms"], expected)
