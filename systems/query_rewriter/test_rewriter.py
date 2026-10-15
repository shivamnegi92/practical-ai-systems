import unittest

from systems.query_rewriter.app import BM25, expand_query, search

CORPUS = {
    "d1": "Costs are eight dollars monthly.",
    "d3": "Cancel requests take one business day.",
}


class QueryRewriterTests(unittest.TestCase):
    def test_expand_query_adds_known_synonym(self):
        self.assertIn("cost", expand_query("What is the price?"))

    def test_expand_query_leaves_unknown_terms_alone(self):
        self.assertEqual(expand_query("weather today"), "weather today")

    def test_baseline_misses_synonym_only_match(self):
        hits = search(CORPUS, "price information please", expand=False)
        self.assertEqual(hits, [])

    def test_expansion_recovers_the_match(self):
        hits = search(CORPUS, "price information please", expand=True)
        self.assertTrue(hits)
        self.assertEqual(hits[0][0], "d1")


if __name__ == "__main__":
    unittest.main()


class MorphologyEvaluation(unittest.TestCase):
    def test_stemming_prevents_two_dictionary_expansions(self):
        for query in ["pricing information", "erasing my files"]:
            self.assertEqual(expand_query(query),query)
        self.assertIn("delete",expand_query("remove my files"))
        from systems.query_rewriter.evaluate import evaluate
        self.assertEqual(evaluate()["cases"],10)
        self.assertLess(evaluate()["recall_at_1_expanded"],1)
