import unittest
from systems.multimodal_ocr.app import normalize_lines, extract_fields

class OCRTests(unittest.TestCase):
 def test_sort_and_validate_boxes(self):
  lines=normalize_lines([{'text':'later','bbox':[1,20,3,25]},{'text':'first','bbox':[1,1,3,5]},{'text':'bad','bbox':[0,0,-2,1]}])
  self.assertEqual([x['text'] for x in lines],['first','later'])
 def test_extract_fields(self):
  fields=extract_fields([{'text':'Invoice # X-2','bbox':[0,0,50,10]},{'text':'Total: $4.00','bbox':[0,10,50,20]}])
  self.assertEqual(fields['invoice_number'],'X-2'); self.assertEqual(fields['total'],'4.00')
