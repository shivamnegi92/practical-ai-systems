import unittest
from systems.invoice_extract.app import extract

class AmountBoundaryTests(unittest.TestCase):
 def test_does_not_extract_a_valid_looking_prefix_of_bad_amount(self):
  for field in ('Subtotal','Tax','Total'):
   for amount in ('12.345','12.000','1.23.45','1.23,45'):
    with self.subTest(field=field,amount=amount):
     invoice=extract(f'{field}: ${amount}')
     self.assertIsNone(getattr(invoice,field.lower()))
     self.assertIn(f'missing:{field.lower()}',invoice.errors)
 def test_normal_cents_and_trailing_punctuation_are_preserved(self):
  for suffix in ('','.',', paid'):
   self.assertEqual(extract('Total: $12.34'+suffix).total,'12.34')
