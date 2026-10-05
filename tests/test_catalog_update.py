import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from catalog_update import render_catalog, validate_catalog


def make_entry(**overrides):
    entry = {
        "name": "Example",
        "url": "https://github.com/example/project",
        "category": "agents",
        "kind": "framework",
        "summary": "Build a useful AI system.",
        "tradeoff": "Review operational complexity.",
        "archived": False,
        "stars": {"count": 420, "observed_at": "2026-10-05"},
        "license": {"spdx": "Apache-2.0", "status": "verified", "evidence": "https://github.com/example/project/blob/main/LICENSE"},
        "origin": {"status": "screened", "evidence": "Owner and project origin checked."},
        "discovery": {
            "source": "https://github.com/trending",
            "observed_at": "2026-10-05",
            "basis": "Trending page observation",
        },
    }
    entry.update(overrides)
    return entry


class ValidateCatalogTests(unittest.TestCase):
    def test_accepts_a_complete_entry(self):
        errors = validate_catalog({"entries": [make_entry()]})
        self.assertEqual(errors, [])

    def test_rejects_duplicate_repository_urls(self):
        errors = validate_catalog({"entries": [make_entry(), make_entry(name="Duplicate")]})
        self.assertTrue(any("duplicate URL" in error for error in errors))

    def test_rejects_unreviewed_origin(self):
        entry = make_entry(origin={"status": "needs_review", "evidence": "unclear"})
        errors = validate_catalog({"entries": [entry]})
        self.assertTrue(any("origin" in error.lower() for error in errors))

    def test_rejects_unverified_license(self):
        entry = make_entry(license={"spdx": "UNKNOWN", "status": "unverified", "evidence": "unknown"})
        errors = validate_catalog({"entries": [entry]})
        self.assertTrue(any("license" in error.lower() for error in errors))

    def test_rejects_missing_license_evidence(self):
        entry = make_entry(license={"spdx": "Apache-2.0", "status": "verified"})
        errors = validate_catalog({"entries": [entry]})
        self.assertTrue(any("license" in error.lower() for error in errors))

    def test_rejects_disallowed_project_origin(self):
        entry = make_entry(origin={"status": "excluded", "evidence": "Policy conflict"})
        errors = validate_catalog({"entries": [entry]})
        self.assertTrue(any("origin" in error.lower() for error in errors))

    def test_rejects_archived_repository(self):
        errors = validate_catalog({"entries": [make_entry(archived=True)]})
        self.assertTrue(any("archived" in error.lower() for error in errors))

    def test_rejects_missing_trend_observation(self):
        entry = make_entry(discovery={"source": "https://github.com/trending", "basis": "top"})
        errors = validate_catalog({"entries": [entry]})
        self.assertTrue(any("observed_at" in error for error in errors))

    def test_rejects_invalid_star_snapshot(self):
        entry = make_entry(stars={"count": -3, "observed_at": "2026-10-05"})
        errors = validate_catalog({"entries": [entry]})
        self.assertTrue(any("stars" in error.lower() for error in errors))


class RenderCatalogTests(unittest.TestCase):
    def test_renders_categories_and_entries_inside_markers(self):
        readme = "Before\n<!-- TRENDING-CATALOG:START -->\nold\n<!-- TRENDING-CATALOG:END -->\nAfter\n"
        rendered = render_catalog(readme, {"entries": [make_entry()]})
        self.assertIn("### Agents and orchestration", rendered)
        self.assertIn("[Example](https://github.com/example/project)", rendered)
        self.assertTrue(rendered.startswith("Before\n"))
        self.assertTrue(rendered.endswith("After\n"))

    def test_fails_when_catalog_markers_are_missing(self):
        with self.assertRaises(ValueError):
            render_catalog("No markers here", {"entries": [make_entry()]})

    def test_render_is_idempotent_and_replaces_old_generated_content(self):
        readme = "Before\n<!-- TRENDING-CATALOG:START -->\nold generated section\n<!-- TRENDING-CATALOG:END -->\nAfter\n"
        catalog = {"entries": [make_entry()]}
        once = render_catalog(readme, catalog)
        twice = render_catalog(once, catalog)
        self.assertEqual(once, twice)
        self.assertNotIn("old generated section", twice)
        self.assertEqual(twice.count("[Example](https://github.com/example/project)"), 1)

    def test_preserves_content_outside_generated_region(self):
        readme = "Custom introduction\n<!-- TRENDING-CATALOG:START -->\nold\n<!-- TRENDING-CATALOG:END -->\nHandwritten conclusion\n"
        rendered = render_catalog(readme, {"entries": [make_entry()]})
        self.assertIn("Custom introduction", rendered)
        self.assertIn("Handwritten conclusion", rendered)

    def test_does_not_duplicate_repository_already_in_readme(self):
        readme = "Existing [Example](https://github.com/example/project)\n<!-- TRENDING-CATALOG:START -->\n<!-- TRENDING-CATALOG:END -->\n"
        with self.assertRaisesRegex(ValueError, "already present"):
            render_catalog(readme, {"entries": [make_entry()]})


if __name__ == "__main__":
    unittest.main()
