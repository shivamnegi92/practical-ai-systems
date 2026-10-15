import unittest

from systems.dedupe_questions.app import find_duplicates, similarity


class DedupeTests(unittest.TestCase):
    def test_identical_meaning_is_high_similarity(self):
        score = similarity("How do I reset my password?", "How can I reset my password?")
        self.assertGreaterEqual(score, 0.6)

    def test_unrelated_questions_are_low_similarity(self):
        score = similarity("What is your refund policy?", "Where is my order?")
        self.assertLess(score, 0.3)

    def test_empty_strings_are_identical(self):
        self.assertEqual(similarity("", ""), 1.0)

    def test_find_duplicates_returns_index_pairs(self):
        pairs = find_duplicates(["Reset my password", "Please reset my password", "Where is my order?"])
        self.assertIn((0, 1), [(i, j) for i, j, _ in pairs])


if __name__ == "__main__":
    unittest.main()


class EvaluationLimits(unittest.TestCase):
    def test_negation_false_positive_and_paraphrase_false_negative(self):
        self.assertGreaterEqual(similarity("How do I enable email alerts?", "How do I not enable email alerts?"), 0.6)
        self.assertLess(similarity("How do I activate notifications?", "How do I enable alerts?"), 0.6)
        from systems.dedupe_questions.evaluate import evaluate
        self.assertEqual(evaluate()["cases"], 13)
        self.assertLess(evaluate()["f1"], 1)
