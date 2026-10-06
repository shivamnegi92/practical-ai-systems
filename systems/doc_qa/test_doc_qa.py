import unittest

from common.llm import StubLLM
from systems.doc_qa.app import DocQA, load_chunks
from systems.doc_qa.evaluate import evaluate


class DocQATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qa = DocQA(load_chunks())

    def test_chunks_carry_source_ids(self):
        ids = [chunk_id for chunk_id, _ in load_chunks()]
        self.assertIn("billing.md#2", ids)
        self.assertEqual(len(ids), len(set(ids)))

    def test_answers_with_citation(self):
        answer = self.qa.answer("How much does the Pro plan cost?")
        self.assertIn("$8", answer.text)
        self.assertEqual(answer.citations[0], "billing.md#1")
        self.assertFalse(answer.abstained)

    def test_abstains_when_no_evidence(self):
        answer = self.qa.answer("Does the app integrate with Salesforce CRM?")
        self.assertTrue(answer.abstained)
        self.assertEqual(answer.citations, [])

    def test_llm_mode_uses_only_retrieved_context(self):
        llm = StubLLM(lambda prompt: "Pro costs $8 per user per month [billing.md#1]")
        answer = DocQA(load_chunks(), llm=llm).answer("How much does the Pro plan cost?")
        self.assertIn("billing.md#1", llm.calls[0])
        self.assertIn("$8", answer.text)
        self.assertEqual(answer.citations, ["billing.md#1"])

    def test_llm_reply_without_valid_citation_is_rejected(self):
        llm = StubLLM(lambda prompt: "It is free forever.")
        answer = DocQA(load_chunks(), llm=llm).answer("How much does the Pro plan cost?")
        self.assertTrue(answer.abstained)

    def test_evaluation_metrics_are_in_range(self):
        metrics = evaluate()["metrics"]
        self.assertGreaterEqual(metrics["recall_at_3"], 0.8)
        for value in metrics.values():
            self.assertTrue(0 <= value <= 1)


if __name__ == "__main__":
    unittest.main()
