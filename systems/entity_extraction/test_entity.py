import unittest
from systems.entity_extraction.app import extract, score

class EntityTests(unittest.TestCase):
 def test_known_places_keep_exact_spans_and_people(self):
  for place in ('New York', 'San Francisco', 'Los Angeles', 'New Delhi', 'New  York'):
   text=f'Meeting in {place} with Dr. Ana Li.'
   with self.subTest(place=place):
    entities=extract(text)
    self.assertIn({'text':place,'type':'LOCATION','start':11,'end':11+len(place)},entities)
    self.assertIn('Ana Li',[e['text'] for e in entities if e['type']=='PERSON'])
    self.assertEqual([text[e['start']:e['end']] for e in entities],[e['text'] for e in entities])
 def test_extracts_and_offsets_are_exact(self):
  text='Maya Chen approved $2,500.00 on March 4, 2026.'
  entities=extract(text)
  self.assertEqual([text[e['start']:e['end']] for e in entities],[e['text'] for e in entities])
  self.assertIn({'text':'Maya Chen','type':'PERSON','start':0,'end':9},entities)
 def test_exact_span_metrics(self):
  gold=[{'text':'Maya Chen','type':'PERSON'}]
  self.assertEqual(score(gold,gold)['f1'],1)
  self.assertEqual(score([],gold)['recall'],0)
