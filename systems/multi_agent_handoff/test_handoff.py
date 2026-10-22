import unittest

from systems.multi_agent_handoff.app import handle


class MultiAgentHandoffTests(unittest.TestCase):
    def test_resolves_clear_billing_request(self):
        result = handle({"text": "There is a refund issue with my invoice payment."})
        self.assertEqual(result["status"], "resolved")
        self.assertEqual(result["category"], "billing")

    def test_resolves_clear_technical_request(self):
        result = handle({"text": "My password login keeps showing an error and the app crashes."})
        self.assertEqual(result["status"], "resolved")
        self.assertEqual(result["category"], "technical")

    def test_escalates_unknown_category(self):
        result = handle({"text": "Can you tell me about your company history?"})
        self.assertEqual(result["status"], "escalated")
        self.assertIsNone(result["category"])

    def test_escalates_low_confidence_match(self):
        result = handle({"text": "There was an error."})
        self.assertEqual(result["status"], "escalated")
        self.assertEqual(result["category"], "technical")


if __name__ == "__main__":
    unittest.main()


class AmbiguousHandoffEvaluation(unittest.TestCase):
    def test_ties_resolve_instead_of_escalating_and_repetition_stays_low(self):
        for text in ["refund payment error crash", "password username error crash"]:
            self.assertEqual(handle({"text": text})["status"], "resolved")
        self.assertEqual(handle({"text": "error error error"})["status"], "escalated")
        from systems.multi_agent_handoff.evaluate import evaluate
        self.assertEqual(evaluate()["cases"], 13)
        self.assertEqual(evaluate()["routing_accuracy"], round(11/13,4))
