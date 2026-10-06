"""Minimal MCP JSON-RPC tool server over stdio (tools/list and tools/call)."""
from __future__ import annotations
import json
import sys
from common.text import BM25
from systems.doc_qa.app import load_chunks

class KnowledgeTools:
    def __init__(self):
        self.chunks = dict(load_chunks())
        self.index = BM25(self.chunks)

    def search(self, query: str, limit: int = 3) -> dict:
        hits = self.index.search(query, max(1, min(limit, 10)))
        return {"results": [{"id": chunk_id, "text": self.chunks[chunk_id], "score": round(score, 4)} for chunk_id, score in hits]}

    def read(self, chunk_id: str) -> dict:
        if chunk_id not in self.chunks:
            raise ValueError("unknown chunk id")
        return {"id": chunk_id, "text": self.chunks[chunk_id]}


def _tool_definitions() -> list[dict]:
    return [
        {
            "name": "search_docs",
            "description": "Search the bundled synthetic docs",
            "inputSchema": {
                "type": "object",
                "properties": {"query": {"type": "string"}, "limit": {"type": "integer"}},
                "required": ["query"],
            },
        },
        {
            "name": "read_chunk",
            "description": "Read one retrieved chunk by id",
            "inputSchema": {
                "type": "object",
                "properties": {"chunk_id": {"type": "string"}},
                "required": ["chunk_id"],
            },
        },
    ]


def _call_tool(params: dict, tools: KnowledgeTools) -> dict:
    name = params.get("name")
    arguments = params.get("arguments", {})
    try:
        if name == "search_docs":
            result = tools.search(**arguments)
        elif name == "read_chunk":
            result = tools.read(**arguments)
        else:
            raise ValueError("unknown tool")
        return {"content": [{"type": "text", "text": json.dumps(result)}]}
    except (TypeError, ValueError) as exc:
        return {"content": [{"type": "text", "text": str(exc)}], "isError": True}


def dispatch(message: dict, tools: KnowledgeTools) -> dict:
    method = message.get("method")
    params = message.get("params", {})
    request_id = message.get("id")
    if method == "initialize":
        result = {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "local-knowledge-base", "version": "0.1.0"},
        }
    elif method == "notifications/initialized":
        return {}
    elif method == "tools/list":
        result = {"tools": _tool_definitions()}
    elif method == "tools/call":
        result = _call_tool(params, tools)
    else:
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "method not found"}}
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def main() -> None:
    tools = KnowledgeTools()
    for line in sys.stdin:
        try:
            request = json.loads(line)
            response = dispatch(request, tools)
            if response:
                print(json.dumps(response), flush=True)
        except (ValueError, TypeError) as exc:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}), flush=True)


if __name__ == "__main__":
    main()
