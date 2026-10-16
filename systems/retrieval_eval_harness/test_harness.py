import unittest

from systems.retrieval_eval_harness.app import evaluate_ranking, reciprocal_rank, recall_at_k, ndcg_at_k


class RetrievalEvalHarnessTests(unittest.TestCase):
    def test_ndcg_does_not_credit_the_same_document_twice(self):
        self.assertEqual(ndcg_at_k(['a','a'],{'a':1},2),1)
        for k in (2,3):
            self.assertEqual(ndcg_at_k(['a','a','b'],{'a':2,'b':1},k),
                             ndcg_at_k(['a','missing','b'],{'a':2,'b':1},k))
        self.assertEqual(ndcg_at_k(['a','b'],{'a':2,'b':1},2),1)
        self.assertEqual(ndcg_at_k(['missing','missing'],{'a':1},2),0)
        self.assertEqual(ndcg_at_k(['a','a'],{'a':0},2),0)

    def test_unjudged_object_names_remain_zero_gain(self):
        self.assertAlmostEqual(ndcg_at_k(['constructor','a'],{'a':1},2),0.6309297535714575)
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
