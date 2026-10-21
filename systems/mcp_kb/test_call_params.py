import json
from pathlib import Path
import subprocess
import sys
import unittest
from systems.mcp_kb.server import KnowledgeTools, dispatch


class CallParamsTests(unittest.TestCase):
    def test_named_call_params_must_be_an_object(self):
        for params in (None, [], ['read_chunk'], 'bad', 7, True):
            with self.subTest(params=params):
                response = dispatch({'id': 'bad-call', 'method': 'tools/call', 'params': params}, KnowledgeTools())
                self.assertEqual(response, {'jsonrpc':'2.0','id':'bad-call','error':{'code':-32602,'message':'params must be an object'}})
        response = dispatch({'id':1,'method':'tools/call','params':{'name':'read_chunk','arguments':{'chunk_id':'accounts.md#1'}}},KnowledgeTools())
        self.assertNotIn('isError', response['result'])

    def test_bad_params_do_not_terminate_the_stdio_server(self):
        messages = [{'id':1,'method':'tools/call','params':None},
                    {'id':2,'method':'tools/call','params':[]},
                    {'id':3,'method':'tools/list'}]
        result = subprocess.run([sys.executable,'-m','systems.mcp_kb.server'],
                                cwd=Path(__file__).resolve().parents[2],
                                input=''.join(json.dumps(m)+'\n' for m in messages),
                                text=True,capture_output=True,timeout=15)
        self.assertEqual(result.returncode,0,result.stderr)
        responses=[json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual([r['id'] for r in responses],[1,2,3])
        self.assertEqual([r['error']['code'] for r in responses[:2]],[-32602,-32602])
        self.assertEqual(len(responses[2]['result']['tools']),2)
