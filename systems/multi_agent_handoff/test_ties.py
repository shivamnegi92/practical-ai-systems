import unittest
from systems.multi_agent_handoff.app import handle, triage


class TieTests(unittest.TestCase):
    def test_ties_never_call_a_specialist(self):
        for text, score in [("invoice payment error login", 2),
                            ("invoice payment error login username profile", 2),
                            ("invoice error", 1), ("hello", 0)]:
            with self.subTest(text=text):
                self.assertEqual(triage(text), (None, score))
                self.assertEqual(handle({"text": text}),
                                 {"status": "escalated", "category": None, "confidence": score})

    def test_unique_winner_with_runner_up_still_routes(self):
        self.assertEqual(handle({"text": "invoice payment refund error login"})["category"], "billing")
        self.assertEqual(handle({"text": "invoice payment error login crash"})["category"], "technical")
