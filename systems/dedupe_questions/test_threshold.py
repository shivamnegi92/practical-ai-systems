import subprocess,sys,unittest
from pathlib import Path
from systems.dedupe_questions.app import find_duplicates

class ThresholdTests(unittest.TestCase):
 def test_threshold_is_validated_even_without_question_pairs(self):
  for questions in ([],['same question','same question']):
   for value in (-.1,1.1,float('nan'),float('inf'),True,None,'0.5'):
    with self.subTest(questions=questions,value=value),self.assertRaisesRegex(ValueError,'threshold'):find_duplicates(questions,value)
  self.assertEqual(find_duplicates(['same question','same question'],1),[(0,1,1.0)])
  self.assertEqual(len(find_duplicates(['cats','dogs'],0)),1)
 def test_cli_reports_invalid_threshold_without_a_traceback(self):
  root=Path(__file__).resolve().parents[2]
  for value in ('nan','-0.1','1.1'):
   result=subprocess.run([sys.executable,'-m','systems.dedupe_questions.app','same question','same question','--threshold',value],cwd=root,capture_output=True,text=True,timeout=15)
   self.assertEqual(result.returncode,2,result.stderr)
   self.assertIn('threshold',result.stderr);self.assertNotIn('Traceback',result.stderr)
