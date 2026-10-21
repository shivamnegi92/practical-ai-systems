import unittest
from decimal import localcontext
from systems.invoice_extract.app import extract

def invoice(total):
 return "Vendor: Demo\nInvoice: INV-1\nDate: 2026-01-01\nSubtotal: 1000000000000000000000000000000.00\nTax: 0.01\nTotal: "+total+"\n"
class ExactCents(unittest.TestCase):
 def test_large_one_cent_mismatch_is_not_rounded_away(self):
  self.assertIn("mismatch:total",extract(invoice("1000000000000000000000000000000.00")).errors)
 def test_large_correct_sum_is_accepted(self):
  self.assertEqual(extract(invoice("1000000000000000000000000000000.01")).errors,[])
 def test_callers_decimal_precision_is_preserved(self):
  with localcontext() as ctx:
   ctx.prec=4
   self.assertEqual(extract(invoice("1000000000000000000000000000000.01")).errors,[])
   self.assertEqual(ctx.prec,4)
