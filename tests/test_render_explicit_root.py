import json
import tempfile
import unittest
from pathlib import Path
from scripts.render_systems import render_readme, START, END

class ExplicitRoot(unittest.TestCase):
 def test_renderer_uses_manifests_from_the_supplied_root(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);folder=root/"systems/custom_demo";folder.mkdir(parents=True)
   (folder/"system.json").write_text(json.dumps({"title":"Custom fixture","level":"Beginner","order":1,"prerequisites":"Python","hook":"Local demo"}))
   (folder/"README.md").write_text("A fixture")
   (folder/"evaluate.py").write_text("")
   (folder/"eval").mkdir()
   (folder/"eval/results.json").write_text(json.dumps({"system":"custom_demo","method":"offline","dataset":{"cases":1},"metrics":{"accuracy":1}}))
   text="Prefix\n"+START+"\nold\n"+END+"\nSuffix"
   rendered=render_readme(text,root=root)
   self.assertIn("Custom fixture",rendered)
   self.assertIn("systems/custom_demo/README.md",rendered)
   self.assertNotIn("systems/bounded_agent/",rendered)
   self.assertTrue(rendered.startswith("Prefix\n"))
   self.assertTrue(rendered.endswith("\nSuffix"))
   self.assertEqual(render_readme(rendered,root=root),rendered)
