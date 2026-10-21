import unittest

from systems.multi_hop_router.app import answer_multi_hop, decompose


class MultiHopRouterTests(unittest.TestCase):
    def test_decompose_splits_on_and(self):
        parts = decompose("How much does the Pro plan cost and how often do notes sync?")
        self.assertEqual(len(parts), 2)

    def test_answers_when_every_sub_question_is_answerable(self):
        result = answer_multi_hop("How much does the Pro plan cost and how often do notes sync?")
        self.assertFalse(result["abstained"])
        self.assertIn("billing.md#1", result["citations"])
        self.assertIn("sync.md#1", result["citations"])

    def test_abstains_when_any_sub_question_is_unanswerable(self):
        result = answer_multi_hop(
            "How much does the Pro plan cost and does Lumen Notes integrate with Salesforce CRM?"
        )
        self.assertTrue(result["abstained"])

    def test_handles_two_separately_punctuated_questions(self):
        result = answer_multi_hop("How often do notes sync? How do I reset my password?")
        self.assertFalse(result["abstained"])

    def test_abstains_on_empty_or_question_marks_only(self):
        for blank in ["", "   ", "???", "  ? and ?  "]:
            with self.subTest(blank=blank):
                result = answer_multi_hop(blank)
                self.assertTrue(result["abstained"])
                self.assertIsNone(result["answer"])
                self.assertEqual(result["citations"], [])


if __name__ == "__main__":
    unittest.main()
