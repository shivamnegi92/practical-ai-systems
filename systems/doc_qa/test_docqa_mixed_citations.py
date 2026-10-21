import unittest
from systems.doc_qa.app import DocQA, StubLLM
class MixedCitationTests(unittest.TestCase):
 def make(self,reply):
  return DocQA([('known','Orbit costs ten dollars.')],llm=StubLLM(lambda _:reply),min_score=0,min_coverage=0)
 def test_mixed_unknown_citation_abstains(self):
  result=self.make('Orbit costs ten dollars [known]. Extra claim [invented].').answer('Orbit cost?')
  self.assertTrue(result.abstained)
  self.assertEqual(result.citations,[])
 def test_all_known_citations_remain_deduplicated(self):
  result=self.make('Orbit [known] costs ten dollars [known].').answer('Orbit cost?')
  self.assertFalse(result.abstained)
  self.assertEqual(result.citations,['known'])
 def test_uncited_still_abstains(self):
  self.assertTrue(self.make('Orbit costs ten dollars.').answer('Orbit cost?').abstained)
