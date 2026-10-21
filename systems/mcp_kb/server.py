"""Minimal MCP JSON-RPC tool server over stdio (tools/list and tools/call)."""
from __future__ import annotations
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

_STOPWORDS = frozenset(
    "a an and are as at be by can do does for from has have how i in is it its of on or "
    "our that the their this to was we what when where which who why will with you your".split()
)
_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _stem(token: str) -> str:
    for suffix in ("ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 2 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def tokenize(text: str) -> list[str]:
    return [_stem(t) for t in _TOKEN_RE.findall(text.lower()) if t not in _STOPWORDS]


class BM25:
    """Okapi BM25 over a {doc_id: text} mapping."""

    def __init__(self, docs: dict[str, str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tokens = {doc_id: tokenize(text) for doc_id, text in docs.items()}
        self.avg_len = sum(map(len, self.tokens.values())) / max(len(self.tokens), 1)
        df = Counter(term for toks in self.tokens.values() for term in set(toks))
        n = len(self.tokens)
        self.idf = {term: math.log(1 + (n - freq + 0.5) / (freq + 0.5)) for term, freq in df.items()}

    def score(self, query: str, doc_id: str) -> float:
        toks = self.tokens[doc_id]
        counts = Counter(toks)
        norm = self.k1 * (1 - self.b + self.b * len(toks) / (self.avg_len or 1))
        return sum(
            self.idf[t] * counts[t] * (self.k1 + 1) / (counts[t] + norm)
            for t in set(tokenize(query))
            if t in counts
        )

    def search(self, query: str, k: int = 5) -> list[tuple[str, float]]:
        scored = ((doc_id, self.score(query, doc_id)) for doc_id in self.tokens)
        hits = sorted((h for h in scored if h[1] > 0), key=lambda h: (-h[1], h[0]))
        return hits[:k]


def load_chunks(data_dir: Path = DATA_DIR) -> list[tuple[str, str]]:
    """Split each markdown file into paragraph chunks with stable ids (file#n)."""
    chunks = []
    for path in sorted(data_dir.glob("*.md")):
        paragraphs = [p.strip() for p in path.read_text().split("\n\n") if p.strip() and not p.startswith("#")]
        chunks += [(f"{path.name}#{i}", text) for i, text in enumerate(paragraphs, start=1)]
    return chunks


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
    if not isinstance(message, dict) or not isinstance(message.get("method"), str):
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "invalid request"}}
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
