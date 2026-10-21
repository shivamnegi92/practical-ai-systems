import unittest
from systems.caption_qc.app import check_caption
class WordContent(unittest.TestCase):
 def test_punctuation_cannot_satisfy_minimum(self):
  for text in ("!!! ??? ...","A cat !!!", "-- _ ."):
   with self.subTest(text=text):self.assertIn("too_short",check_caption(text)["reasons"])
 def test_real_words_and_numbers_still_count(self):
  self.assertTrue(check_caption("Three red cars.")["passed"])
  self.assertTrue(check_caption("2 red cars.")["passed"])
 def test_punctuation_does_not_consume_maximum_budget(self):
  self.assertNotIn("too_long",check_caption("Three red cars " + "! "*30)["reasons"])
