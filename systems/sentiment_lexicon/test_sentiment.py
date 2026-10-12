import unittest

from systems.sentiment_lexicon.app import classify


class SentimentLexiconTests(unittest.TestCase):
    def test_negation_flips_each_polarity(self):
        for text, expected in (("This is not good", "negative"), ("not bad at all", "positive"),
                               ("never good", "negative"), ("no good", "negative"),
                               ("isn't good", "negative"), ("isn’t bad", "positive")):
            with self.subTest(text=text):
                self.assertEqual(classify(text), expected)

    def test_negation_window_is_three_previous_tokens(self):
        self.assertEqual(classify("not at all good"), "negative")
        self.assertEqual(classify("not really at all good"), "positive")

    def test_non_negation_apostrophe_keeps_existing_word_matches(self):
        self.assertEqual(classify("good's meaning"), "positive")

    def test_positive_words_win(self):
        self.assertEqual(classify("This product is great and the support team is fantastic."), "positive")

    def test_negative_words_win(self):
        self.assertEqual(classify("The checkout process is slow and confusing."), "negative")

    def test_no_lexicon_words_is_neutral(self):
        self.assertEqual(classify("It's okay, does the job."), "neutral")

    def test_tied_counts_default_to_neutral(self):
        self.assertEqual(classify("I love this app but the login page is terrible."), "neutral")


if __name__ == "__main__":
    unittest.main()
