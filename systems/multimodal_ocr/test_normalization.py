import unittest
from systems.multimodal_ocr.app import normalize_lines

class NormalizationTests(unittest.TestCase):
 def test_rejects_nonfinite_and_boolean_coordinates(self):
  for bad in (float('nan'), float('inf'), float('-inf'), True, False):
   for index in range(4):
    box=[0,0,10,10]; box[index]=bad
    with self.subTest(bad=bad,index=index):
     self.assertEqual(normalize_lines([{'text':'bad','bbox':box}]),[])
 def test_null_text_is_empty_and_finite_signed_boxes_still_work(self):
  self.assertEqual(normalize_lines([{'text':None,'bbox':[0,0,1,1]}]),[])
  self.assertEqual(normalize_lines([{'text':' ok ','bbox':[-2,-1,0,1]}]),[{'text':'ok','bbox':[-2.,-1.,0.,1.]}])
