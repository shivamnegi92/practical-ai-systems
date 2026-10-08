import json
import tempfile
import unittest
from pathlib import Path
from scripts.evaluate_systems import SYSTEMS, normalize, run_all, validate
from scripts.render_systems import render_readme

ROOT = Path(__file__).resolve().parents[1]


class SystemEvaluationTests(unittest.TestCase):
    def test_every_system_has_valid_evidence_packet(self):
        results = run_all()
        self.assertEqual(set(results), set(SYSTEMS))
        self.assertEqual(validate(results), [])

    def test_rejects_missing_case_count(self):
        with self.assertRaises(ValueError):
            normalize("broken", {"metrics": {"f1": 1.0}})

    def test_committed_results_match_fresh_run(self):
        for name, result in run_all().items():
            with self.subTest(system=name):
                committed = json.loads((ROOT / "systems" / name / "eval" / "results.json").read_text())
                self.assertEqual(committed, result)

    def test_readme_render_is_idempotent_and_limited_to_markers(self):
        readme = (ROOT / "README.md").read_text()
        rendered = render_readme(readme)
        self.assertEqual(render_readme(rendered), rendered)
        self.assertIn("## Pick your starting point", rendered)
        self.assertIn("### Beginner", rendered)
        self.assertIn("### Intermediate", rendered)
        self.assertIn("### Advanced", rendered)
        self.assertIn("#### [Voice-agent transcript evaluator]", rendered)
        self.assertLess(rendered.index("### Beginner"), rendered.index("## Learning paths"))
        self.assertIn("## Run your first project", rendered)
        self.assertNotIn("<!-- SYSTEMS:START -->\n<!-- SYSTEMS:END -->", rendered)

    def test_duplicate_markers_are_rejected(self):
        readme = (ROOT / "README.md").read_text()
        with self.assertRaises(ValueError):
            render_readme(readme + "\n<!-- SYSTEMS:START -->\n<!-- SYSTEMS:END -->\n")


if __name__ == "__main__":
    unittest.main()
