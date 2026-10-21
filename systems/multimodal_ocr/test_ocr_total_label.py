import unittest
from systems.multimodal_ocr.app import extract_fields
class LabelTests(unittest.TestCase):
 def test_subtotal_is_not_total(self):
  self.assertIsNone(extract_fields([{'text':'Subtotal: $12.00','bbox':[0,0,10,10]}])['total'])
 def test_real_total_after_subtotal(self):
  rows=[{'text':'Subtotal: $12.00','bbox':[0,0,10,10]}, {'text':'Total: $15.00','bbox':[0,20,10,30]}]
  self.assertEqual(extract_fields(rows)['total'],'15.00')
 def test_grand_total_is_supported(self):
  self.assertEqual(extract_fields([{'text':'Grand Total: $15.00','bbox':[0,0,10,10]}])['total'],'15.00')
