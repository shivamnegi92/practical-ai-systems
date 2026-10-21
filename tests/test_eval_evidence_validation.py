import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import evaluate_systems as ev

class EvidenceValidation(unittest.TestCase):
 def packet(self,cases=1,metric=0.5):return {"system":"demo","method":"offline","dataset":{"cases":cases},"metrics":{"score":metric}}
 def test_boolean_case_count_is_not_a_workload(self):
  self.assertTrue(ev.validate({"demo":self.packet(cases=True)},("demo",)))
 def test_nonfinite_and_nonnumeric_metrics_are_rejected(self):
  for value in (float("nan"),float("inf"),"high",None):
   with self.subTest(value=value):self.assertTrue(ev.validate({"demo":self.packet(metric=value)},("demo",)))
 def test_boolean_flags_and_finite_metrics_remain_supported(self):
  for value in (0,0.5,True):self.assertEqual(ev.validate({"demo":self.packet(metric=value)},("demo",)),[])
 def test_check_write_does_not_overwrite_existing_results_on_validation_error(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);path=root/"systems/demo/eval/results.json";path.parent.mkdir(parents=True);path.write_text("previous evidence")
   with patch.object(ev,"ROOT",root),patch.object(ev,"SYSTEMS",("demo",)),patch.object(ev,"run_all",return_value={"demo":self.packet(cases=0)}),patch("sys.argv",["evaluate_systems.py","--check","--write","--only","demo"]),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
    self.assertEqual(ev.main(),1)
   self.assertEqual(path.read_text(),"previous evidence")
