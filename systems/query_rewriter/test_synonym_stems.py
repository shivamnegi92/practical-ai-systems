import unittest
from systems.query_rewriter.app import expand_query, BM25

class SynonymStemTests(unittest.TestCase):
 def test_declared_pricing_alias_is_reachable_after_tokenization(self):
  query='What is the PRICING?'
  expanded=expand_query(query)
  self.assertTrue(expanded.startswith(query))
  self.assertIn('cost',expanded.split())
  self.assertEqual(BM25({'billing':'cost'}).search(expanded,1)[0][0],'billing')
 def test_existing_aliases_and_unknown_query_are_preserved(self):
  self.assertEqual(expand_query('unknown'), 'unknown')
  self.assertIn('cancel',expand_query('unsubscribe').split())
  self.assertIn('delete',expand_query('remove').split())
  self.assertEqual(expand_query('price').split().count('cost'),1)
