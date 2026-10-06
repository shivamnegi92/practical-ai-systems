import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_catalog import check_generated, render_paths, render_readme, validate_paths


class DecisionPathTests(unittest.TestCase):
    def setUp(self):
        self.paths = json.loads((ROOT / "catalog" / "paths.json").read_text())
        self.projects = json.loads((ROOT / "catalog" / "projects.json").read_text())

    def test_paths_use_existing_project_ids_and_paths(self):
        for path in self.paths:
            for step in path["steps"]:
                for project_id in step["project_ids"]:
                    self.assertIn(project_id, {record["id"] for record in self.projects})
                for link in step["links"]:
                    if link.startswith(("https://", "http://")):
                        continue
                    self.assertTrue((ROOT / link).exists(), link)

    def test_rejects_non_string_path_id_without_crashing(self):
        path = json.loads(json.dumps(self.paths[0]))
        path["id"] = []
        errors = validate_paths([path], self.projects, ROOT)
        self.assertTrue(any("id" in error.lower() for error in errors))

    def test_rejects_unknown_project_id(self):
        path = json.loads(json.dumps(self.paths[0]))
        path["steps"][0]["project_ids"] = ["nobody/missing"]
        errors = validate_paths([path], self.projects, ROOT)
        self.assertTrue(any("unknown project ID" in error for error in errors))

    def test_rejects_missing_local_guide(self):
        path = json.loads(json.dumps(self.paths[0]))
        path["steps"][0]["links"] = ["recipes/missing/README.md"]
        errors = validate_paths([path], self.projects, ROOT)
        self.assertTrue(any("missing local path" in error for error in errors))

    def test_renders_path_as_ordered_steps(self):
        rendered = render_paths(self.paths, self.projects)
        self.assertIn("# Build a document-search baseline", rendered)
        self.assertIn("## 1. Define representative questions", rendered)
        self.assertIn("[Docling](https://github.com/docling-project/docling)", rendered)
        self.assertIn("](../recipes/document-search/README.md)", rendered)
        self.assertIn("](../catalog/extraction.md)", rendered)

    def test_readme_renders_generated_paths_section(self):
        readme = "Intro\n<!-- SYSTEMS:START --><!-- SYSTEMS:END -->\n<!-- CATALOG:START -->\n<!-- CATALOG:END -->\n## Choose a path\n<!-- PATHS:START -->\n<!-- PATHS:END -->\nFooter\n"
        rendered = render_readme(readme, self.projects, self.paths)
        self.assertIn("Build a document-search baseline", rendered)
        self.assertIn("catalog/paths.md#build-a-document-search-baseline", rendered)
        self.assertIn("Intro", rendered)
        self.assertIn("Footer", rendered)

    def test_readme_renderer_requires_both_regions_without_overlap(self):
        from build_catalog import render_readme

        with self.assertRaisesRegex(ValueError, "overlap"):
            render_readme("<!-- SYSTEMS:START --><!-- SYSTEMS:END --><!-- CATALOG:START -->text<!-- PATHS:START -->middle<!-- PATHS:END -->more<!-- CATALOG:END -->", self.projects, self.paths)

    def test_readme_renderer_rejects_duplicate_markers(self):
        from build_catalog import render_readme

        readme = "<!-- SYSTEMS:START --><!-- SYSTEMS:END --><!-- CATALOG:START --><!-- CATALOG:END --><!-- CATALOG:START --><!-- CATALOG:END --><!-- PATHS:START --><!-- PATHS:END -->"
        with self.assertRaisesRegex(ValueError, "exactly one"):
            render_readme(readme, self.projects, self.paths)

    def test_paths_output_is_up_to_date(self):
        self.assertEqual(check_generated(ROOT), [])



if __name__ == "__main__":
    unittest.main()
