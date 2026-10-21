import tempfile
import unittest
from pathlib import Path
from systems.repo_guard.app import scan


class PemHeaderTests(unittest.TestCase):
    def test_private_key_labels_are_reported_once_on_the_right_line(self):
        for label in ("PRIVATE KEY", "RSA PRIVATE KEY", "EC PRIVATE KEY",
                      "OPENSSH PRIVATE KEY", "ENCRYPTED PRIVATE KEY"):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / "synthetic.pem").write_text("synthetic header fixture only\n-----BEGIN " + label + "-----\nNOT-A-KEY\n", encoding="utf-8")
                self.assertEqual(scan(root), [{"file": "synthetic.pem", "line": 2, "kind": "private key"}])

    def test_public_and_incomplete_headers_are_not_private_keys(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "public.pem").write_text("\n".join([
                "-----BEGIN PUBLIC KEY-----", "-----BEGIN RSA PUBLIC KEY-----",
                "-----BEGIN CERTIFICATE-----", "-----BEGIN ENCRYPTED PUBLIC KEY-----",
                "-----BEGIN ENCRYPTED PRIVATE KEY", "-----END ENCRYPTED PRIVATE KEY-----",
            ]), encoding="utf-8")
            self.assertEqual(scan(root), [])
