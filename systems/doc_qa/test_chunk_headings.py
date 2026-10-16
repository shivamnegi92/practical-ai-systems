import tempfile,unittest
from pathlib import Path
from systems.doc_qa.app import load_chunks

class HeadingBodyTests(unittest.TestCase):
 def chunks(self,text):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder);(p/'guide.md').write_text(text,encoding='utf-8')
   return load_chunks(p)
 def test_heading_and_body_in_same_paragraph_keeps_the_body(self):
  self.assertEqual(self.chunks('# Heading\nUseful body.'),[('guide.md#1','Useful body.')])
  self.assertEqual(self.chunks('### Heading\nÇağrı örneği.'),[('guide.md#1','Çağrı örneği.')])
 def test_heading_only_and_existing_paragraph_ids_are_preserved(self):
  self.assertEqual(self.chunks('# Heading\n\nFirst.\n\nSecond.'),[('guide.md#1','First.'),('guide.md#2','Second.')])
  self.assertEqual(self.chunks('# Heading'),[])
 def test_hash_prefixed_content_and_fenced_code_are_not_headings(self):
  self.assertEqual(self.chunks('#hashtag body'),[('guide.md#1','#hashtag body')])
  self.assertEqual(self.chunks('```\n# literal\n```'),[('guide.md#1','```\n# literal\n```')])
