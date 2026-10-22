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


class RetrievalEvaluationLimits(unittest.TestCase):
    def test_synonym_queries_have_no_hits_without_query_expansion(self):
        tools = KnowledgeTools()
        for query in ["forgotten credentials", "paid tier price"]:
            self.assertEqual(tools.search(query)["results"], [])
        from systems.mcp_kb.evaluate import evaluate
        self.assertEqual(evaluate()["cases"], 10)
        self.assertLess(evaluate()["recall_at_3"], 1)
