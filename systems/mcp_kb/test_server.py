import unittest
from systems.mcp_kb.server import KnowledgeTools, dispatch

class MCPTests(unittest.TestCase):
 def test_tools_list_and_call(self):
  tools=KnowledgeTools()
  listed=dispatch({'id':1,'method':'tools/list'},tools)
  self.assertEqual(len(listed['result']['tools']),2)
  called=dispatch({'id':2,'method':'tools/call','params':{'name':'search_docs','arguments':{'query':'password reset'}}},tools)
  self.assertIn('accounts.md',called['result']['content'][0]['text'])
 def test_unknown_tool_returns_error_content(self):
  result=dispatch({'id':3,'method':'tools/call','params':{'name':'delete_everything','arguments':{}}},KnowledgeTools())
  self.assertTrue(result['result']['isError'])
