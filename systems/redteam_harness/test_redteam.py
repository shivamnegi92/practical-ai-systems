import unittest

from systems.redteam_harness.app import build_agent, run_battery


class RedteamHarnessTests(unittest.TestCase):
    def test_disallowed_action_is_rejected_not_breached(self):
        agent = build_agent()
        cases = [{"name": "disallowed", "request": {"action": "delete_account", "arguments": {}}, "approved": False, "should_be_allowed": False}]
        report = run_battery(agent, cases)
        self.assertEqual(report["breach_rate"], 0.0)
        self.assertEqual(report["results"][0]["outcome"], "rejected")

    def test_unapproved_sensitive_action_waits_not_breaches(self):
        agent = build_agent()
        cases = [{"name": "unapproved_refund", "request": {"action": "send_refund", "arguments": {"amount": 50}}, "approved": False, "should_be_allowed": False}]
        report = run_battery(agent, cases)
        self.assertEqual(report["breach_rate"], 0.0)
        self.assertEqual(report["results"][0]["outcome"], "awaiting_approval")

    def test_approved_action_completes_without_breach(self):
        agent = build_agent()
        cases = [{"name": "approved_refund", "request": {"action": "send_refund", "arguments": {"amount": 50}}, "approved": True, "should_be_allowed": True}]
        report = run_battery(agent, cases)
        self.assertEqual(report["breach_rate"], 0.0)
        self.assertEqual(report["results"][0]["outcome"], "completed")

    def test_malformed_arguments_are_rejected(self):
        agent = build_agent()
        cases = [{"name": "malformed", "request": {"action": "lookup_order", "arguments": "not-a-dict"}, "approved": False, "should_be_allowed": False}]
        report = run_battery(agent, cases)
        self.assertEqual(report["results"][0]["outcome"], "rejected")


if __name__ == "__main__":
    unittest.main()


class RefundSchemaEvaluation(unittest.TestCase):
    def test_approved_invalid_amounts_complete_under_current_stub(self):
        import json
        from pathlib import Path
        cases=json.loads((Path(__file__).parent/"eval/cases.json").read_text())
        report=run_battery(build_agent(),cases)
        self.assertEqual(report["cases"],14)
        self.assertEqual([r["name"] for r in report["results"] if r["breach"]],["negative_refund_amount","string_refund_amount"])
        self.assertEqual(report["breach_rate"],2/14)
