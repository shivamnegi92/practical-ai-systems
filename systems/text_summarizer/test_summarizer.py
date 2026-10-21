import unittest

from systems.text_summarizer.app import compression_ratio, sentences, summarize


class SummarizerTests(unittest.TestCase):
    def test_abbreviations_keep_the_complete_example_sentence(self):
        text = "Dr. Smith arrived at 3 p.m. today. He left. The end."
        self.assertEqual(sentences(text), ["Dr. Smith arrived at 3 p.m. today.", "He left.", "The end."])
        self.assertEqual(summarize(text, n=1), ["Dr. Smith arrived at 3 p.m. today."])

    def test_fixed_abbreviation_list_and_case(self):
        for abbreviation in ("Dr.", "Mr.", "Mrs.", "Ms.", "e.g.", "i.e.", "a.m.", "p.m.", "etc.", "DR."):
            with self.subTest(abbreviation=abbreviation):
                self.assertEqual(sentences(f"Use {abbreviation} here. Next!"), [f"Use {abbreviation} here.", "Next!"])

    def test_ordinary_boundaries_and_abbreviation_suffix_control(self):
        self.assertEqual(sentences("Really? Yes! Ready. Done."), ["Really?", "Yes!", "Ready.", "Done."])
        self.assertEqual(sentences("Notadr. Next."), ["Notadr.", "Next."])
        self.assertEqual(sentences(""), [])

    def test_short_text_returned_unchanged(self):
        self.assertEqual(summarize("One sentence only."), ["One sentence only."])

    def test_picks_sentence_with_frequent_terms(self):
        text = (
            "Database indexing speeds up queries. "
            "Indexing indexing indexing is crucial for performance. "
            "The weather was nice yesterday."
        )
        summary = summarize(text, n=1)
        self.assertIn("indexing", summary[0].lower())

    def test_compression_ratio_is_fraction_of_original(self):
        text = "Short sentence one. Short sentence two. Short sentence three."
        summary = summarize(text, n=1)
        ratio = compression_ratio(text, summary)
        self.assertGreater(ratio, 0)
        self.assertLess(ratio, 1)

    def test_empty_text_has_zero_ratio(self):
        self.assertEqual(compression_ratio("", []), 0.0)


if __name__ == "__main__":
    unittest.main()
