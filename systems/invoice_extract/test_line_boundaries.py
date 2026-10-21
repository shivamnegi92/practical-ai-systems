import unittest
from systems.invoice_extract.app import extract

class LineBoundaryTests(unittest.TestCase):
 def test_empty_vendor_does_not_consume_the_next_field(self):
  for newline in ('\n','\r\n'):
   invoice=extract(f'Vendor:  {newline}Invoice: X-1{newline}Date: 2026-01-01')
   self.assertIsNone(invoice.vendor)
   self.assertIn('missing:vendor',invoice.errors)
   self.assertEqual(invoice.invoice_number,'X-1')
 def test_blank_vendor_is_missing(self):
  self.assertIsNone(extract('Vendor:   ').vendor)
 def test_amount_values_do_not_cross_line_boundaries(self):
  for field in ('Subtotal','Tax','Total'):
   invoice=extract(f'{field}:\n12.00')
   self.assertIsNone(getattr(invoice,field.lower()))
   self.assertIn(f'missing:{field.lower()}',invoice.errors)
 def test_horizontal_whitespace_and_crlf_remain_supported(self):
  invoice=extract('Vendor:\tAcme\r\nInvoice No:\tX-1\r\nDate:\t2026-01-01\r\nSubtotal:\t$10.00\r\nTax:\t$2.00\r\nTotal:\t$12.00\r\n')
  self.assertEqual(invoice.vendor,'Acme')
  self.assertEqual(invoice.errors,[])
