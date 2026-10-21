import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from systems.repo_guard.app import scan
class UppercaseSuffixTests(unittest.TestCase):
 def test_uppercase_and_mixed_case_shell_files(self):
  with TemporaryDirectory() as d:
   root=Path(d)
   for name in ['build.SH','workflow.YML','config.YaMl']:
    (root/name).write_text('chmod 777 /tmp/example',encoding='utf-8')
   self.assertEqual({x['file'] for x in scan(root)}, {'build.SH','workflow.YML','config.YaMl'})
 def test_text_file_does_not_become_shell(self):
  with TemporaryDirectory() as d:
   (Path(d)/'notes.txt').write_text('chmod 777 /tmp/example',encoding='utf-8')
   self.assertEqual(scan(Path(d)),[])
