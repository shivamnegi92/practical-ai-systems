import unittest
from systems.judge_audit.judge import judge
class NumberSupport(unittest.TestCase):
 def test_mismatched_numbers_cannot_be_supported_by_shared_words(self):
  for claim,evidence in (("The plan costs 80 dollars per month","The plan costs 8 dollars per month"),("The fee is 8.50 dollars","The fee is 8.05 dollars"),("Keep 30 days of history","Keep 300 days of history")):
   with self.subTest(claim=claim):self.assertEqual(judge(claim,evidence),"unsupported")
 def test_matching_numbers_and_ordinary_claims(self):
  self.assertEqual(judge("The plan costs 8 dollars","The plan costs 8 dollars per month"),"supported")
  self.assertEqual(judge("History lasts 30 days","History lasts 30 days for 8 users"),"supported")
  self.assertEqual(judge("Exports support PDF","Exports support PDF"),"supported")
