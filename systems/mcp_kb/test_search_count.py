import unittest
from systems.mcp_kb.server import BM25

class SearchCountTests(unittest.TestCase):
 def test_result_count_is_a_nonnegative_integer(self):
  for docs in ({},{'a':'term','b':'term'}):
   index=BM25(docs)
   for k in (-1,1.5,float('nan'),float('inf'),True):
    with self.subTest(docs=docs,k=k),self.assertRaisesRegex(ValueError,'nonnegative integer'):index.search('term',k)
   self.assertEqual(index.search('term',0),[])
   self.assertEqual(len(index.search('term',5)),len(docs))
   self.assertEqual(len(index.search('term',1)),min(1,len(docs)))
