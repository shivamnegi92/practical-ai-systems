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

    def test_different_stopword_only_questions_are_not_duplicates(self):
        self.assertEqual(similarity("Who are you?", "What is it?"), 0.0)
        self.assertEqual(similarity("What is it?", "what is it"), 1.0)
        self.assertEqual(find_duplicates(["Who are you?", "What is it?"]), [])

    def test_find_duplicates_returns_index_pairs(self):
        pairs = find_duplicates(["Reset my password", "Please reset my password", "Where is my order?"])
        self.assertIn((0, 1), [(i, j) for i, j, _ in pairs])


if __name__ == "__main__":
    unittest.main()
