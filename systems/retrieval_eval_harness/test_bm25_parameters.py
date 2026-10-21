import unittest
from systems.retrieval_eval_harness.app import BM25
class ParameterTests(unittest.TestCase):
 def test_invalid_configuration_refused_before_search(self):
  for name,values in [('k1',[-1,float('nan'),float('inf'),True,'1',10**1000]),('b',[-0.1,1.1,float('nan'),float('inf'),True,'0.5'])]:
   for value in values:
    with self.subTest(name=name,value=str(value)[:30]),self.assertRaises(ValueError):
     BM25({'one':'orbit docs'},**{name:value})
 def test_boundary_values_and_empty_corpus(self):
  for b in [0,1]:
   self.assertEqual(BM25({'one':'orbit docs'},k1=0,b=b).search('orbit')[0][0],'one')
   self.assertEqual(BM25({},k1=0,b=b).search('orbit'),[])
