import unittest

from systems.citation_checker.app import check_citations

CHUNKS = {
    "billing.md#1": "The Pro plan costs 8 dollars per user per month.",
    "sync.md#1": "Notes sync automatically every 60 seconds while online.",
}


class CitationCheckerTests(unittest.TestCase):
    def test_changed_numeric_facts_are_unsupported_with_a_reason(self):
        pairs = [
            ('The Pro plan costs $80 per user per month.', 'The Pro plan costs $8 per user per month.'),
            ('The deadline is 2026-01-02.', 'The deadline is 2026-01-01.'),
            ('The discount rate is 20%.', 'The discount rate is 2%.'),
            ('The quota allows 80 requests.', 'The quota allows 8 requests.'),
            ('The average duration is 1.50 seconds.', 'The average duration is 1.05 seconds.'),
            ('The Pro plan costs €8 per user per month.', 'The Pro plan costs $8 per user per month.'),
        ]
        for claim, source in pairs:
            with self.subTest(claim=claim):
                row=check_citations(claim[:-1]+' [ref#99].', {'ref#99':source})['results'][0]
                self.assertEqual(row['status'],'unsupported')
                self.assertEqual(row['reason'],'number_mismatch')

    def test_matching_numbers_ignore_numeric_citation_ids(self):
        claim='The Pro plan costs $8 and renews on 2026-01-01 with a 2% discount'
        report=check_citations(claim+' [ref#99].', {'ref#99':claim+'.'})
        self.assertTrue(report['all_supported'])
    def test_supported_citation(self):
        report = check_citations("The Pro plan costs 8 dollars per month [billing.md#1].", CHUNKS)
        self.assertEqual(report["results"][0]["status"], "supported")

    def test_fabricated_claim_is_unsupported(self):
        report = check_citations("Refunds are available within 90 days [billing.md#1].", CHUNKS)
        self.assertEqual(report["results"][0]["status"], "unsupported")

    def test_unknown_chunk_id_is_flagged(self):
        report = check_citations("Exports support CSV format [sharing.md#5].", CHUNKS)
        self.assertEqual(report["results"][0]["status"], "unknown_chunk")

    def test_answer_without_citations_is_vacuously_all_supported(self):
        report = check_citations("No citations here.", CHUNKS)
        self.assertEqual(report["citations"], 0)
        self.assertTrue(report["all_supported"])


if __name__ == "__main__":
    unittest.main()
