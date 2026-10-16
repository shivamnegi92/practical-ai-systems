import unittest
from systems.semantic_cache.cache import SemanticCache

class CacheTests(unittest.TestCase):
 def test_embedded_delimiters_do_not_alias_namespace_fields(self):
  triples=[('q','a','b\0c'),('q','a\0b','c'),('c\0q','a','b')]
  c=SemanticCache()
  self.assertEqual(len({c.key(*triple) for triple in triples}),3)
  for i,(query,model,version) in enumerate(triples):c.put(query,str(i),model,version)
  for i,(query,model,version) in enumerate(triples):self.assertEqual(c.get(query,model,version),str(i))
 def test_normalization_with_quoted_namespace_values_is_preserved(self):
  c=SemanticCache();c.put(' Hello  WORLD ','ok','model"\\name','version\n1')
  self.assertEqual(c.get('hello world','model"\\name','version\n1'),'ok')
  self.assertIsNone(c.get('hello world','model"\\name','other'))
 def test_normalized_exact_match_and_model_isolation(self):
  c=SemanticCache(); c.put(' Hello  world ','yes')
  self.assertEqual(c.get('hello world'),'yes')
  self.assertIsNone(c.get('hello world',model='other'))
 def test_lru_eviction(self):
  c=SemanticCache(max_entries=2); c.put('a','1'); c.put('b','2'); c.get('a'); c.put('c','3')
  self.assertIsNone(c.get('b')); self.assertEqual(c.get('a'),'1')
 def test_expiry(self):
  now=[0.0]; c=SemanticCache(ttl_seconds=5,clock=lambda:now[0]); c.put('a','x'); now[0]=6
  self.assertIsNone(c.get('a'))
