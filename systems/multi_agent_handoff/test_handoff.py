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

    def test_missing_text_key_escalates(self):
        result = handle({})
        self.assertEqual(result["status"], "escalated")
        self.assertIsNone(result["category"])

    def test_invalid_request_or_text_raises_type_error(self):
        for bad_req in [None, "text", ["text"], {"text": None}, {"text": 123}]:
            with self.subTest(bad_req=bad_req):
                with self.assertRaises(TypeError):
                    handle(bad_req)


if __name__ == "__main__":
    unittest.main()
