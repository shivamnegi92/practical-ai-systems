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

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
