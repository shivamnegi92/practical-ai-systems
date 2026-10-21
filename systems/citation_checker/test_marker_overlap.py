import unittest
from systems.citation_checker.app import check_citations


class MarkerOverlapTests(unittest.TestCase):
    def test_ids_do_not_change_claim_overlap(self):
        for chunk_id in ("short", "long-document-id-with-many-words-100"):
            row = check_citations(f"Orbit [{chunk_id}].", {chunk_id: "Orbit"}, .8)["results"][0]
            self.assertEqual((row["status"], row["overlap"]), ("supported", 1))

    def test_marker_words_cannot_supply_support(self):
        row = check_citations("Elsewhere [orbit].", {"orbit": "Orbit"})["results"][0]
        self.assertEqual((row["status"], row["overlap"]), ("unsupported", 0))
        self.assertFalse(check_citations("[orbit]", {"orbit": "Orbit"}, 0)["all_supported"])

    def test_each_marker_uses_the_same_unannotated_claim(self):
        rows = check_citations("Orbit [alpha] [beta].", {"alpha": "Orbit", "beta": "Unrelated"})["results"]
        self.assertEqual([r["overlap"] for r in rows], [1, 0])
        self.assertEqual(check_citations("Orbit [unknown].", {})["results"][0]["status"], "unknown_chunk")
