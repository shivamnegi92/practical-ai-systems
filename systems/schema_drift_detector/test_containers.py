import unittest
from systems.schema_drift_detector.app import detect_drift, infer_type

class ContainerTypeTests(unittest.TestCase):
 def test_json_container_names_and_legacy_aliases(self):
  for kind,values in [('array',[[],[1]]),('list',[[],[1]]),('object',[{}, {'x':1}]),('dict',[{}, {'x':1}])]:
   for value in values:
    with self.subTest(kind=kind,value=value):
     self.assertFalse(detect_drift({'value':{'type':kind,'required':True}},[{'value':value}])['drift_detected'])
 def test_arrays_and_objects_are_not_interchangeable(self):
  for kind,value in [('array',{}),('list',{}),('object',[]),('dict',[])]:
   self.assertEqual(detect_drift({'value':{'type':kind}},[{'value':value}])['type_mismatched_fields'],['value'])
 def test_null_required_and_existing_python_helper_spelling_are_preserved(self):
  self.assertEqual(infer_type([]),'list');self.assertEqual(infer_type({}),'dict')
  result=detect_drift({'value':{'type':'array','required':True}},[{'value':None}])
  self.assertEqual(result['missing_required_fields'],['value'])
  self.assertEqual(result['type_mismatched_fields'],[])
