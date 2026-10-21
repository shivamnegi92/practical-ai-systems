import json
import subprocess
import sys
import unittest
from systems.mcp_kb.server import KnowledgeTools, dispatch


class ArgumentTypeTests(unittest.TestCase):
    def test_invalid_values_are_tool_errors(self):
        tools = KnowledgeTools()
        for name, arguments in [
            *[("search_docs", {"query": value}) for value in (None, 7, True, [], {})],
            *[("search_docs", {"query": "password", "limit": value}) for value in (None, True, "3", 1.5, float("nan"), float("inf"))],
            *[("read_chunk", {"chunk_id": value}) for value in (None, 7, True, [], {})],
        ]:
            with self.subTest(name=name, arguments=arguments):
                result = dispatch({"id": 4, "method": "tools/call", "params": {"name": name, "arguments": arguments}}, tools)
                self.assertEqual(result["id"], 4)
                self.assertTrue(result["result"].get("isError"))

    def test_bad_query_does_not_stop_stdio(self):
        messages = [{"id": 1, "method": "tools/call", "params": {"name": "search_docs", "arguments": {"query": 7}}},
                    {"id": 2, "method": "tools/list"}]
        result = subprocess.run([sys.executable, "-m", "systems.mcp_kb.server"], input="".join(json.dumps(m) + "\n" for m in messages), capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        responses = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual([r["id"] for r in responses], [1, 2])
        self.assertTrue(responses[0]["result"]["isError"])
        self.assertEqual(len(responses[1]["result"]["tools"]), 2)

    def test_default_and_integral_limits_keep_clamping(self):
        tools = KnowledgeTools()
        self.assertEqual(tools.search("password", 1.0), tools.search("password", 1))
        self.assertEqual(tools.search("password", -1), tools.search("password", 1))
        self.assertTrue(tools.search("password")["results"])
