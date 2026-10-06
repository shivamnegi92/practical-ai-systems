import unittest

from examples.lexical_retrieval_baseline.retrieve import rank_documents


class RankDocumentsTests(unittest.TestCase):
    def test_ranks_relevant_document_above_unrelated_document(self):
        documents = {
            "policy": "Employees can request parental leave through the HR portal.",
            "weather": "The store expects rain and cooler temperatures tomorrow.",
        }
        results = rank_documents("How do I request parental leave?", documents)
        self.assertEqual(results[0][0], "policy")

    def test_returns_empty_results_for_blank_query(self):
        self.assertEqual(rank_documents("   ", {"doc": "Some text"}), [])

    def test_limits_results_and_omits_zero_overlap(self):
        documents = {
            "one": "blue berry and apple",
            "two": "blue berry",
            "three": "orange fruit",
        }
        results = rank_documents("blue berry", documents, top_k=1)
        self.assertEqual(len(results), 1)
        self.assertIn(results[0][0], {"one", "two"})
        self.assertEqual(results[0][1], 1.0)

    def test_rejects_non_positive_top_k(self):
        with self.assertRaises(ValueError):
            rank_documents("search", {"doc": "search"}, top_k=0)


if __name__ == "__main__":
    unittest.main()
