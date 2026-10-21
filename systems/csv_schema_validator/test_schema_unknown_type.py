import unittest
from systems.csv_schema_validator.app import validate_row,validate_rows
class SchemaTypeTests(unittest.TestCase):
 def test_unknown_types_are_configuration_errors(self):
  for kind in ['numbr','integer',None,[]]:
   for row in [{},{'value':'accepted before'}]:
    with self.subTest(kind=kind,row=row), self.assertRaises(ValueError):
     validate_row({'value':{'type':kind}},row)
   with self.assertRaises(ValueError): validate_rows({'value':{'type':kind}},[])
 def test_supported_and_omitted_types(self):
  self.assertEqual(validate_row({'a':{'type':'number'},'b':{'type':'boolean'},'c':{}},{'a':1,'b':False,'c':'text'}),[])
