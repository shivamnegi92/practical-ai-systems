import unittest

from systems.retrieval_eval_harness.app import evaluate_ranking, reciprocal_rank, recall_at_k


class RetrievalEvalHarnessTests(unittest.TestCase):
    def test_recall_at_k_counts_relevant_hits(self):
        self.assertEqual(recall_at_k(["a", "b", "c"], {"b"}, 3), 1.0)
        self.assertEqual(recall_at_k(["a", "c"], {"b"}, 3), 0.0)

    def test_reciprocal_rank_rewards_earlier_hits(self):
        self.assertEqual(reciprocal_rank(["a", "b", "c"], {"b"}), 0.5)
        self.assertEqual(reciprocal_rank(["a", "c"], {"b"}), 0.0)

    def test_evaluate_ranking_combines_metrics(self):
        result = evaluate_ranking(["a", "b", "c"], {"a": 0, "b": 1, "c": 0}, k=3)
        self.assertEqual(result["recall_at_k"], 1.0)
        self.assertEqual(result["mrr"], 0.5)
        self.assertAlmostEqual(result["ndcg_at_k"], 0.6309, places=3)


if __name__ == "__main__":
    unittest.main()


class MultiRelevantEvaluation(unittest.TestCase):
    def test_two_relevant_documents_and_unmatched_synonyms(self):
        import json
        from pathlib import Path
        from systems.retrieval_eval_harness.app import compare_strategies
        from systems.retrieval_eval_harness.evaluate import evaluate
        data=json.loads((Path(__file__).parent/"eval/cases.json").read_text())
        both=compare_strategies(data["corpus"],[{"text":"business day","relevance":{"d3":1,"d4":1}}])
        self.assertEqual(both["expanded"]["recall_at_k"],1)
        for text,gold in [("membership tariff","d1"),("end subscription","d3")]:
            report=compare_strategies(data["corpus"],[{"text":text,"relevance":{gold:1}}])
            self.assertEqual(report["expanded"]["recall_at_k"],0)
        self.assertEqual(evaluate()["cases"],11)
