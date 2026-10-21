import unittest
from systems.readability_scorer.app import grade_level, sentences
class EmptySentenceFragments(unittest.TestCase):
 def test_punctuation_does_not_dilute_sentence_length(self):
  text="The organization evaluates complex international obligations."
  self.assertEqual(grade_level("!!! ??? ... "+text),grade_level(text))
  self.assertEqual(grade_level(text+" !!! ??? ..."),grade_level(text))
 def test_no_lexical_sentence_for_punctuation_only(self):
  self.assertEqual(sentences("!!! ??? ..."),[])
  self.assertEqual(grade_level("!!! ??? ..."),0)
 def test_real_sentences_are_preserved(self):
  self.assertEqual(sentences("One sentence. Another sentence!"),["One sentence.","Another sentence!"])
