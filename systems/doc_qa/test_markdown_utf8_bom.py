import tempfile
import unittest
from pathlib import Path
from systems.doc_qa.app import load_chunks

class Utf8Markdown(unittest.TestCase):
 def test_bom_heading_does_not_become_a_retrieval_chunk(self):
  with tempfile.TemporaryDirectory() as tmp:
   (Path(tmp)/"policy.md").write_bytes("\ufeff# Caf\u00e9 policy\n\nCancellation costs \u20ac5.".encode("utf-8"))
   self.assertEqual(load_chunks(Path(tmp)),[("policy.md#1","Cancellation costs \u20ac5.")])
 def test_plain_utf8_body_is_preserved(self):
  with tempfile.TemporaryDirectory() as tmp:
   (Path(tmp)/"policy.md").write_bytes("# Policy\n\nCaf\u00e9 costs \u20ac5.".encode("utf-8"))
   self.assertEqual(load_chunks(Path(tmp)),[("policy.md#1","Caf\u00e9 costs \u20ac5.")])
