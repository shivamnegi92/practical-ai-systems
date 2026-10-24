import json
import unittest
from pathlib import Path
from systems.invoice_extract.app import extract

class InvoiceTests(unittest.TestCase):
    def test_us_thousands_separators_preserve_fields_and_validate_balance(self):
        text = 'Vendor: A\nInvoice: 1\nDate: 2026-01-01\nSubtotal: 1,000.00\nTax: 80.00\nTotal: 1,080.00'
        invoice = extract(text)
        self.assertEqual(invoice.subtotal, '1,000.00')
        self.assertEqual(invoice.total, '1,080.00')
        self.assertEqual(invoice.errors, [])
        self.assertEqual(extract(text.replace('1,080.00', '1,090.00')).errors, ['mismatch:total'])
    def test_schema_and_total_validation(self):
        cases = json.loads((Path(__file__).parent / "eval" / "cases.json").read_text())
        for case in cases:
            with self.subTest(case=case):
                result = extract(case["text"])
                self.assertEqual({k: getattr(result,k) for k in case["fields"]}, case["fields"])
                self.assertEqual(not result.errors, case["valid"])
    def test_empty_input_reports_all_missing_fields(self):
        result = extract("")
        self.assertEqual(len(result.errors), 6)

if __name__ == "__main__": unittest.main()
