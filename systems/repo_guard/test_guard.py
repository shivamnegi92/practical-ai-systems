import tempfile
import unittest
from pathlib import Path
from systems.repo_guard.app import scan

class RepoGuardTests(unittest.TestCase):
 def test_detects_private_key_and_ignores_venv(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); (root/'key.pem').write_text('-----BEGIN PRIVATE KEY-----')
   (root/'.venv').mkdir(); (root/'.venv'/'hidden.txt').write_text('AKIA1234567890ABCDEF')
   findings=scan(root); self.assertEqual(len(findings),1); self.assertEqual(findings[0]['kind'],'private key')
 def test_clean_tree(self):
  with tempfile.TemporaryDirectory() as d:
   (Path(d)/'readme.md').write_text('plain text')
   self.assertEqual(scan(Path(d)),[])


class EvaluationScannerBoundary(unittest.TestCase):
 def test_evaluation_uses_file_type_and_line_scoped_scanner(self):
  from systems.repo_guard.evaluate import evaluate
  report=evaluate()
  self.assertEqual(report['cases'],8)
  self.assertEqual(report['precision'],1)
  self.assertEqual(report['recall'],4/6)
 def test_cross_line_pattern_is_not_detected_by_the_actual_scanner(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory)
   (root/'split.sh').write_text('chmod\n777 example')
   (root/'example.txt').write_text('chmod 777 example')
   self.assertEqual(scan(root),[])
