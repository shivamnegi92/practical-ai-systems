"""Exercise the advertised quickstart through its real module entry point."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]


class InvoiceCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, '-m', 'systems.invoice_extract.app', *args],
                              cwd=ROOT, capture_output=True, text=True, timeout=15)

    def test_readme_quickstart_returns_invoice_json(self):
        result = self.run_cli('systems/invoice_extract/sample.txt')
        self.assertEqual(result.returncode, 0, result.stderr)
        invoice = json.loads(result.stdout)
        self.assertEqual(invoice['invoice_number'], 'NW-1042')
        self.assertEqual(invoice['total'], '108.00')
        self.assertEqual(invoice['errors'], [])

    def test_help_and_missing_argument_use_argparse(self):
        help_result = self.run_cli('--help')
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn('file', help_result.stdout)
        missing = self.run_cli()
        self.assertEqual(missing.returncode, 2)
        self.assertIn('required', missing.stderr)
        self.assertNotIn('Traceback', missing.stderr)
