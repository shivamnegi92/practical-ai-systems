import unittest
from systems.caption_qc.app import check_caption


class PhraseTests(unittest.TestCase):
    def test_placeholder_whitespace_is_normalized(self):
        for phrase in ["IMAGE   OF", "picture\tof", "no caption\navailable", "untitled  image"]:
            with self.subTest(phrase=phrase):
                self.assertTrue(any(r.startswith("banned_phrase:") for r in check_caption(phrase + " a dog running")["reasons"]))

    def test_keywords_match_whole_phrases(self):
        self.assertFalse(check_caption("A scarf hangs outside.", ["car"])["passed"])
        self.assertFalse(check_caption("A red carpet outside.", ["red car"])["passed"])
        self.assertTrue(check_caption("A RED\tCAR waits outside.", ["red  car"])["passed"])
        self.assertTrue(check_caption("A (car) waits outside.", ["car"])["passed"])
        self.assertTrue(check_caption("A C++ manual lies open.", ["C++"])["passed"])

    def test_empty_keywords_are_unsatisfied(self):
        self.assertFalse(check_caption("A dog runs outside.", ["  "])["passed"])

    def test_placeholder_must_have_word_boundaries(self):
        self.assertTrue(check_caption("A sculpture with a miniatureimage of clouds.")["passed"])
