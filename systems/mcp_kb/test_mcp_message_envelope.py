import json
import subprocess
import sys
import unittest
from systems.mcp_kb.server import KnowledgeTools,dispatch
class EnvelopeTests(unittest.TestCase):
 def test_invalid_envelopes(self):
  tools=KnowledgeTools()
  for value in [None,[],42,'text',{}, {'method':3}]:
   with self.subTest(value=value):
    result=dispatch(value,tools)
    self.assertEqual(result['error']['code'],-32600)
    self.assertIsNone(result['id'])
 def test_stdio_continues_after_valid_json_scalars(self):
  data='[]\nnull\n42\n'+json.dumps({'id':7,'method':'tools/list'})+'\n'
  p=subprocess.run([sys.executable,'-m','systems.mcp_kb.server'],input=data,text=True,capture_output=True,timeout=15)
  self.assertEqual(p.returncode,0,p.stderr)
  replies=[json.loads(line) for line in p.stdout.splitlines()]
  self.assertEqual(len(replies),4)
  self.assertTrue(all(x['error']['code']==-32600 for x in replies[:3]))
  self.assertEqual(replies[-1]['id'],7)
  self.assertEqual(len(replies[-1]['result']['tools']),2)
