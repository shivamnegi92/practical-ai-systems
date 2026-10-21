import unittest

from systems.sentiment_lexicon.app import classify


class SentimentLexiconTests(unittest.TestCase):
    def test_positive_words_win(self):
        self.assertEqual(classify("This product is great and the support team is fantastic."), "positive")

    def test_negative_words_win(self):
        self.assertEqual(classify("The checkout process is slow and confusing."), "negative")

    def test_no_lexicon_words_is_neutral(self):
        self.assertEqual(classify("It's okay, does the job."), "neutral")

    def test_tied_counts_default_to_neutral(self):
        self.assertEqual(classify("I love this app but the login page is terrible."), "neutral")

    def test_invalid_type_raises_type_error(self):
        for invalid in [None, 123, ["good"], True]:
            with self.subTest(invalid=invalid):
                with self.assertRaises(TypeError):
                    classify(invalid)


if __name__ == "__main__":
    unittest.main()
