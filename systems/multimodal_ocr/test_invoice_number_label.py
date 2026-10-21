import unittest
from systems.multimodal_ocr.app import extract_fields

def fields(text):return extract_fields([{"text":text,"bbox":[0,0,100,10]}])
class InvoiceNumberLabel(unittest.TestCase):
 def test_other_invoice_headings_are_not_identifiers(self):
  for text in ("Invoice Date: 2026-01-01","Invoice Total: $4.00","Invoice"):
   with self.subTest(text=text):self.assertIsNone(fields(text)["invoice_number"])
 def test_full_number_label_and_abbreviations(self):
  for text in ("Invoice Number: INV-7","Invoice No. INV-7","Invoice # INV-7","Invoice: INV-7"):
   with self.subTest(text=text):self.assertEqual(fields(text)["invoice_number"],"INV-7")
 def test_invoice_must_be_a_separate_word(self):
  self.assertIsNone(fields("Preinvoice: INV-7")["invoice_number"])
