import json
import subprocess
import sys
import unittest

from systems.mcp_kb.server import KnowledgeTools, dispatch


class Notifications(unittest.TestCase):
    def test_no_response_for_known_or_unknown_notifications(self):
        for method in ['tools/list', 'notifications/cancelled', 'unknown-method']:
            with self.subTest(method=method):
                self.assertEqual(dispatch({'jsonrpc': '2.0', 'method': method}, KnowledgeTools()), {})

    def test_invalid_envelopes_are_not_silently_dropped(self):
        messages = [
            {'method': 'tools/list'},
            {'jsonrpc': '1.0', 'method': 'tools/list'},
            {'jsonrpc': None, 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'method': ''},
            {'jsonrpc': '2.0', 'method': 42},
        ]
        for message in messages:
            with self.subTest(message=message):
                response = dispatch(message, KnowledgeTools())
                self.assertEqual(response.get('error', {}).get('code'), -32600)
                self.assertIsNone(response['id'])

    def test_explicit_ids_are_not_notifications(self):
        for request_id in [0, '', None]:
            with self.subTest(request_id=request_id):
                response = dispatch({'jsonrpc': '2.0', 'id': request_id, 'method': 'tools/list'}, KnowledgeTools())
                self.assertEqual(response['id'], request_id)
                self.assertIn('result', response)

    def test_tool_notification_is_processed(self):
        class ObservedTools(KnowledgeTools):
            calls = 0

            def search(self, query, limit=3):
                self.calls += 1
                return super().search(query, limit)

        tools = ObservedTools()
        response = dispatch({'jsonrpc': '2.0', 'method': 'tools/call', 'params': {'name': 'search_docs', 'arguments': {'query': 'reset password'}}}, tools)
        self.assertEqual(tools.calls, 1)
        self.assertEqual(response, {})

    def test_stdio_does_not_write_notification_responses(self):
        messages = [
            {'method': 'tools/list'},
            {'jsonrpc': '1.0', 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'method': 'notifications/cancelled'},
            {'jsonrpc': '2.0', 'id': 7, 'method': 'tools/list'},
        ]
        proc = subprocess.run([sys.executable, '-m', 'systems.mcp_kb.server'], input=''.join(json.dumps(m) + '\n' for m in messages), capture_output=True, text=True, timeout=20)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        replies = [json.loads(line) for line in proc.stdout.splitlines()]
        self.assertEqual(len(replies), 3)
        self.assertEqual([r["error"]["code"] for r in replies[:2]], [-32600, -32600])
        self.assertEqual(replies[2]['id'], 7)
