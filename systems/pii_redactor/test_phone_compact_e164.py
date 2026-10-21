import unittest
from systems.pii_redactor.app import detect,redact
class PhoneTests(unittest.TestCase):
 def test_compact_and_international_numbers(self):
  for value in ['5551234567','+905551234567','+442079460958','(555) 123-4567','555-123-4567']:
   with self.subTest(value=value):
    phones=[x for x in detect('Call '+value+' now.') if x['type']=='phone']
    self.assertEqual([x['match'] for x in phones],[value])
    self.assertEqual(redact('Call '+value+' now.'),'Call [REDACTED:PHONE] now.')
 def test_no_partial_match_in_long_or_embedded_identifier(self):
  for value in ['5551234567890123','x5551234567','5551234567x','+1234567890123456']:
   self.assertEqual([x for x in detect(value) if x['type']=='phone'],[])
