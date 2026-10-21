import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from systems.multi_hop_router.app import load_chunks
class DirectoryTests(unittest.TestCase):
 def test_directory_does_not_interrupt_documents(self):
  with TemporaryDirectory() as d:
   root=Path(d)
   (root/'a-directory.md').mkdir()
   (root/'note.md').write_text('Ordinary body paragraph.',encoding='utf-8')
   self.assertEqual(load_chunks(root),[('note.md#1','Ordinary body paragraph.')])
 def test_only_directories_yields_no_chunks(self):
  with TemporaryDirectory() as d:
   (Path(d)/'directory.md').mkdir()
   self.assertEqual(load_chunks(Path(d)),[])
