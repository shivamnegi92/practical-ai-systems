import unittest
from systems.entity_extraction.app import extract, score

class EntityTests(unittest.TestCase):
 def test_iso_dates_are_independent_of_month_day_suffix(self):
  for text in ('Due 2026-10-16.', 'Due 2026-10-16 12 items', '2026-10-16 and January 5, 2026'):
   dates=[e for e in extract(text) if e['type']=='DATE']
   expected=['2026-10-16']+(['January 5, 2026'] if 'January' in text else [])
   self.assertEqual([e['text'] for e in dates],expected)
   self.assertEqual([text[e['start']:e['end']] for e in dates],expected)
 def test_extracts_and_offsets_are_exact(self):
  text='Maya Chen approved $2,500.00 on March 4, 2026.'
  entities=extract(text)
  self.assertEqual([text[e['start']:e['end']] for e in entities],[e['text'] for e in entities])
  self.assertIn({'text':'Maya Chen','type':'PERSON','start':0,'end':9},entities)
 def test_exact_span_metrics(self):
  gold=[{'text':'Maya Chen','type':'PERSON'}]
  self.assertEqual(score(gold,gold)['f1'],1)
  self.assertEqual(score([],gold)['recall'],0)
