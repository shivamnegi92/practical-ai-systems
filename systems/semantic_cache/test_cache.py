import unittest
from systems.semantic_cache.cache import SemanticCache

class CacheTests(unittest.TestCase):
 def test_apostrophes_and_punctuation_are_normalized(self):
  c=SemanticCache(); c.put("What's the price?",'answer')
  for query in ('whats the price', 'What’s the price!', 'whats, the price.'):
   with self.subTest(query=query): self.assertEqual(c.get(query),'answer')
  self.assertIsNone(c.get('whatstheprice'))
  self.assertIsNone(c.get('whats the prize'))
  self.assertIsNone(c.get('whats the price',version='2'))
 def test_punctuation_preserves_word_boundaries(self):
  c=SemanticCache(); c.put('price,USD','answer')
  self.assertEqual(c.get('price USD'),'answer')
  self.assertIsNone(c.get('priceUSD'))
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
