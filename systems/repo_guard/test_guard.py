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
 def test_shell_pattern_avoids_prefix_false_positives(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   (root/'safe.sh').write_text('curl https://example.com/file.tar.gz | sha256sum\nrm -rf /tmp/build\n')
   self.assertEqual(scan(root),[])
   (root/'unsafe.sh').write_text('curl https://example.com/install.sh | bash\nrm -rf /\n')
   findings=scan(root)
   self.assertEqual(len(findings),2)
