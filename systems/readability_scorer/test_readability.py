import unittest

from systems.readability_scorer.app import band, grade_level


class ReadabilityTests(unittest.TestCase):
    def test_short_text_does_not_have_a_negative_grade(self):
        self.assertEqual(grade_level("Hi"), 0.0)

    def test_punctuation_only_text_has_zero_grade(self):
        self.assertEqual(grade_level("..."), 0.0)

    def test_short_plain_sentences_are_simple(self):
        text = "The cat sat on the mat. It was a hot day."
        self.assertEqual(band(grade_level(text)), "simple")

    def test_dense_long_words_are_complex(self):
        text = (
            "Notwithstanding the aforementioned stipulations, the organization's "
            "multifaceted obligations necessitate comprehensive reevaluation."
        )
        self.assertEqual(band(grade_level(text)), "complex")

    def test_empty_text_has_zero_grade(self):
        self.assertEqual(grade_level(""), 0.0)

    def test_band_boundaries(self):
        self.assertEqual(band(6.0), "simple")
        self.assertEqual(band(6.1), "standard")
        self.assertEqual(band(12.1), "complex")


if __name__ == "__main__":
    unittest.main()
