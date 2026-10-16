import unittest
from systems.semantic_cache.cache import SemanticCache

class CacheTests(unittest.TestCase):
 def test_expired_mru_is_removed_before_a_live_lru_is_evicted(self):
  now=[0]; c=SemanticCache(max_entries=2,ttl_seconds=5,clock=lambda:now[0])
  c.put('expired','old');now[0]=4;c.put('live','keep');c.get('expired')
  now[0]=5;c.put('new','new')
  self.assertEqual(c.stats()['hits'],1);self.assertEqual(c.stats()['misses'],0)
  self.assertEqual(c.get('live'),'keep')
  self.assertEqual(c.get('new'),'new')
  self.assertIsNone(c.get('expired'))
 def test_replacing_expired_entry_starts_a_new_ttl(self):
  now=[0];c=SemanticCache(max_entries=1,ttl_seconds=5,clock=lambda:now[0])
  c.put('a','old');now[0]=5;c.put('a','replacement')
  self.assertEqual(c.get('a'),'replacement');now[0]=10;self.assertIsNone(c.get('a'))
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
