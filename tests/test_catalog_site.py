import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_catalog import render_category, render_readme, validate_records


def project(**overrides):
    record = {
        "id": "example/project",
        "name": "Example Project",
        "url": "https://github.com/example/project",
        "category": "agents",
        "capabilities": ["tool-use"],
        "delivery_modes": ["framework"],
        "summary": "A practical example project.",
        "best_for": ["prototyping workflows"],
        "tradeoffs": ["Requires operational design."],
        "license": {
            "status": "verified",
            "spdx": "MIT",
            "evidence_url": "https://github.com/example/project/blob/HEAD/LICENSE",
        },
        "origin": {
            "status": "screened",
            "evidence_url": "https://example.com/about",
            "basis": "Official project and organization pages reviewed for origin.",
        },
        "maintenance": {"status": "active", "last_reviewed": "2026-10-05"},
        "evidence_level": "metadata-reviewed",
    }
    record.update(overrides)
    return record


class CatalogRecordTests(unittest.TestCase):
    def test_accepts_complete_reviewable_record(self):
        self.assertEqual(validate_records([project()]), [])

    def test_rejects_duplicate_ids_and_urls(self):
        errors = validate_records([project(), project(name="Duplicate")])
        self.assertTrue(any("duplicate id" in error for error in errors))
        self.assertTrue(any("duplicate URL" in error for error in errors))

    def test_rejects_unreviewed_origin(self):
        record = project(origin={"status": "needs-review", "evidence_url": "https://example.com/about", "basis": "Origin is not resolved."})
        self.assertTrue(any("origin" in error.lower() for error in validate_records([record])))

    def test_rejects_screened_origin_without_basis(self):
        record = project(origin={"status": "screened", "evidence_url": "https://example.com/about"})
        self.assertTrue(any("basis" in error.lower() for error in validate_records([record])))

    def test_rejects_unverified_license(self):
        record = project(license={"status": "needs-review"})
        self.assertTrue(any("license" in error.lower() for error in validate_records([record])))

    def test_rejects_api_metadata_as_license_evidence(self):
        record = project(license={"status": "verified", "spdx": "MIT", "evidence_url": "https://api.github.com/repos/example/project"})
        self.assertTrue(any("license" in error.lower() for error in validate_records([record])))

    def test_rejects_unknown_taxonomy_values(self):
        record = project(category="miscellaneous")
        self.assertTrue(any("category" in error.lower() for error in validate_records([record])))

    def test_rejects_unreviewed_maintenance(self):
        record = project(maintenance={"status": "needs-review", "last_reviewed": "2026-10-05"})
        self.assertTrue(any("maintenance" in error.lower() for error in validate_records([record])))

    def test_rejects_malformed_capability_elements(self):
        record = project(capabilities=[{"not": "hashable"}])
        errors = validate_records([record])
        self.assertTrue(any("capabilities" in error.lower() for error in errors))

    def test_rejects_null_delivery_modes_without_crashing(self):
        record = project(delivery_modes=None)
        errors = validate_records([record])
        self.assertTrue(any("delivery_modes" in error.lower() for error in errors))

    def test_validates_trend_observation_when_present(self):
        record = project(trend={"source": "https://github.com/trending", "observed_at": "2026-10-05", "basis": "Observed weekly rank", "rank": 0})
        self.assertTrue(any("rank" in error.lower() for error in validate_records([record])))


class CatalogRenderingTests(unittest.TestCase):
    def test_category_view_shows_use_tradeoff_and_evidence(self):
        markdown = render_category("agents", [project()])
        self.assertIn("Example Project", markdown)
        self.assertIn("prototyping workflows", markdown)
        self.assertIn("Requires operational design.", markdown)
        self.assertIn("metadata-reviewed", markdown)

    def test_empty_category_has_honest_empty_state(self):
        markdown = render_category("multimodal", [])
        self.assertIn("No reviewed entries", markdown)

    def test_unknown_category_is_rejected(self):
        with self.assertRaises(ValueError):
            render_category("miscellaneous", [])

    def test_readme_renderer_updates_only_managed_region(self):
        readme = "Intro\n<!-- CATALOG:START -->\nold\n<!-- CATALOG:END -->\n## Choose a path\n<!-- PATHS:START -->\n<!-- PATHS:END -->\nFooter\n"
        rendered = render_readme(readme, [project()], [])
        self.assertIn("[Agents and orchestration](catalog/agents.md)", rendered)
        self.assertIn("Intro\n", rendered)
        self.assertIn("Footer\n", rendered)
        self.assertNotIn("old", rendered)

    def test_readme_renderer_requires_both_markers(self):
        with self.assertRaises(ValueError):
            render_readme("No markers", [project()], [])


    def test_queued_candidates_are_not_rendered_as_active(self):
        records = json.loads((ROOT / "catalog" / "projects.json").read_text())
        rendered = render_category("agents", records)
        self.assertNotIn("Browser Use", rendered)

    def test_active_records_pass_review_gates_and_held_items_are_separate(self):
        records = json.loads((ROOT / "catalog" / "projects.json").read_text())
        self.assertEqual(validate_records(records), [])
        queue = json.loads((ROOT / "catalog" / "review-queue.json").read_text())
        held_ids = {item["id"] for item in queue}
        self.assertNotIn("browser-use/browser-use", {item["id"] for item in records})
        self.assertNotIn("vllm-project/vllm", {item["id"] for item in records})
        self.assertIn("browser-use/browser-use", held_ids)
        self.assertIn("vllm-project/vllm", held_ids)

    def test_readme_generated_views_are_current(self):
        from build_catalog import check_generated

        self.assertEqual(check_generated(ROOT), [])


if __name__ == "__main__":
    unittest.main()
