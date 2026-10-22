# Local knowledge-base MCP server

Expose read-only search and chunk retrieval over bundled synthetic sample documentation.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.mcp_kb.server
```

## Evaluate and test

```bash
python3 -m systems.mcp_kb.evaluate
python3 -m unittest systems.mcp_kb.test_server
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

The included evaluator finds the expected chunk within top 3 for **4/4** synthetic queries. The server implements a small JSON-RPC/MCP-shaped subset over stdio; it has no third-party MCP SDK and has not been validated against MCP client conformance suites. See [`eval/results.json`](eval/results.json).

## Known limitations

A valid JSON-RPC 2.0 envelope without an `id` is a notification: the server processes a supported
method but emits no response, including for an unknown notification method
([JSON-RPC 2.0 §4.1](https://www.jsonrpc.org/specification#notification)).
Missing/wrong `jsonrpc` versions and invalid methods receive invalid-request
errors (`-32600`); they are never silently discarded as notifications.
Explicit IDs such as `0`, `""` and `null` still receive responses. These narrow
tests cover dispatch and the local stdio stream, not full MCP conformance.

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
