import json
import tempfile
import unittest
from pathlib import Path
from scripts.registry import load_manifests

VALID={"title":"Demo","level":"Beginner","order":1,"prerequisites":"Python","hook":"Try it"}
class ManifestFields(unittest.TestCase):
 def load(self, value):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);folder=root/"systems/demo";folder.mkdir(parents=True)
   (folder/"system.json").write_text(json.dumps(value))
   return load_manifests(root)
 def test_invalid_orders_are_actionable(self):
  for value in ("first",None,True,float("nan"),float("inf")):
   with self.subTest(value=value),self.assertRaisesRegex(ValueError,"demo.*order"):
    self.load({**VALID,"order":value})
 def test_text_fields_are_nonempty_strings(self):
  for field in ("title","hook","prerequisites"):
   for value in (None,42," "):
    with self.subTest(field=field,value=value),self.assertRaisesRegex(ValueError,"demo.*"+field):
     self.load({**VALID,field:value})
 def test_manifest_must_be_an_object(self):
  for value in (None,42,[],"manifest"):
   with self.subTest(value=value),self.assertRaisesRegex(ValueError,"demo.*object"):self.load(value)
 def test_finite_numeric_order_preserves_existing_sort_contract(self):
  self.assertEqual(self.load({**VALID,"order":1.5})["demo"]["order"],1.5)
  self.assertEqual(self.load(VALID)["demo"],VALID)
