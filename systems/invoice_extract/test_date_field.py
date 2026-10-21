import unittest
from systems.invoice_extract.app import extract


class DateFieldTests(unittest.TestCase):
    def test_full_date_field_is_required(self):
        for value in ("2026-01-010", "2026-01-01junk", "2026-01-01T10:00:00", "", "\n2026-01-01"):
            with self.subTest(value=value):
                result = extract("Date: " + value + "\nVendor: Demo\n")
                self.assertIsNone(result.invoice_date)
                self.assertIn("missing:invoice_date", result.errors)

    def test_whitespace_line_endings_and_calendar_controls(self):
        for value in ("0001-01-01", "9999-12-31", "2024-02-29"):
            for newline in ("\n", "\r\n"):
                result = extract("Date:\t" + value + " \t" + newline)
                self.assertEqual(result.invoice_date, value)
                self.assertNotIn("invalid:invoice_date", result.errors)
        self.assertIn("invalid:invoice_date", extract("Date: 0000-01-01\n").errors)
        self.assertIn("invalid:invoice_date", extract("Date: 2026-02-29\n").errors)
