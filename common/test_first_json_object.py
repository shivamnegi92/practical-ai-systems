import unittest
from common.llm import parse_json
class FirstJsonObject(unittest.TestCase):
 def test_multiple_objects_return_the_first(self):
  self.assertEqual(parse_json('First: {"a":1} then {"b":2}'),{"a":1})
 def test_malformed_leading_braces_do_not_hide_a_valid_object(self):
  self.assertEqual(parse_json('A {broken} example then {"a":1}'),{"a":1})
 def test_nested_objects_and_braces_inside_strings(self):
  self.assertEqual(parse_json('Result: {"a":{"b":"}"}} then {"c":3}'),{"a":{"b":"}"}})
 def test_absent_or_incomplete_object(self):
  self.assertIsNone(parse_json('No JSON'))
  self.assertIsNone(parse_json('{"a":'))
