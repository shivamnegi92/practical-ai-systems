import unittest

from systems.pii_redactor.app import detect, redact


class PiiRedactorTests(unittest.TestCase):
    def test_overlapping_email_and_ssn_use_original_offsets_once(self):
        for email in ('123-45-6789@example.com','user.123-45-6789@example.com'):
            text=f'Contact {email} today.'
            self.assertEqual({f['type'] for f in detect(text)}, {'email','ssn'})
            self.assertEqual(redact(text), 'Contact [REDACTED:EMAIL] today.')

    def test_disjoint_matches_and_surrounding_text_survive(self):
        text='📧 user.123-45-6789@example.com; SSN 987-65-4321. End.'
        self.assertEqual(redact(text),'📧 [REDACTED:EMAIL]; SSN [REDACTED:SSN]. End.')
    def test_detects_email(self):
        findings = detect("Contact jane.doe@example.com for help.")
        self.assertEqual([f["type"] for f in findings], ["email"])

    def test_redacts_matches_in_place(self):
        text = "Call (555) 123-4567 now."
        redacted = redact(text)
        self.assertNotIn("123-4567", redacted)
        self.assertIn("[REDACTED:PHONE]", redacted)

    def test_clean_text_has_no_findings(self):
        self.assertEqual(detect("No personal data here, just a meeting at 3pm."), [])

    def test_ssn_pattern_does_not_match_phone(self):
        findings = detect("SSN on file: 123-45-6789.")
        self.assertEqual([f["type"] for f in findings], ["ssn"])

    def test_parenthesized_area_code_is_fully_redacted(self):
        self.assertEqual(redact("Call (555) 123-4567 now."), "Call [REDACTED:PHONE] now.")

    def test_dashed_phone_is_fully_redacted(self):
        self.assertEqual(redact("Call 555-123-4567 now."), "Call [REDACTED:PHONE] now.")


if __name__ == "__main__":
    unittest.main()
