import unittest
from systems.pii_redactor.app import detect, redact
class CompactCard(unittest.TestCase):
 def test_compact_card_shape_is_redacted(self):
  self.assertEqual(redact("Card 4111111111111111."),"Card [REDACTED:CREDIT_CARD].")
 def test_not_a_substring_of_longer_identifiers(self):
  for value in ("41111111111111111","a4111111111111111","4111111111111111b"):
   self.assertFalse(any(x["type"]=="credit_card" for x in detect(value)))
 def test_existing_grouped_forms_keep_exact_span(self):
  for value in ("4111-1111-1111-1111","4111 1111 1111 1111"):
   match=next(x for x in detect("Card "+value+".") if x["type"]=="credit_card")
   self.assertEqual(match["match"],value)
   self.assertEqual((match["start"],match["end"]),(5,5+len(value)))
