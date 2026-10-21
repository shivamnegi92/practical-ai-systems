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

    def test_expand_query_deduplicates_and_skips_present_terms(self):
        self.assertEqual(expand_query("erase or remove account"), "erase or remove account delete")
        self.assertEqual(expand_query("What is the price and cost?"), "What is the price and cost?")


if __name__ == "__main__":
    unittest.main()
