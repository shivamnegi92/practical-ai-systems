import json
import unittest
from pathlib import Path
from systems.invoice_extract.app import extract

class InvoiceTests(unittest.TestCase):
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
