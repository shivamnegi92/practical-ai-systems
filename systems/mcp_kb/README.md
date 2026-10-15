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

The shared ten-query matrix preserves all four original Python and four browser queries and adds two synonym-based misses. The Python evaluator uses all bundled document chunks; the browser retains its four shortened embedded chunks. Results therefore measure different corpus conditions, not identical retrieval systems. See [`eval/results.json`](eval/results.json). This JSON-RPC/MCP-shaped subset has no third-party SDK and has not run MCP client conformance suites.

## Known limitations

- `forgotten credentials` and `paid tier price` have no lexical matches despite corresponding to password reset and Pro pricing. Gold labels retain those desired document IDs without query-expansion tuning. The browser also cannot retrieve `sync.md#3` because that chunk is absent from its embedded corpus; do not hide this miss by changing its gold label. These are retrieval checks, not protocol or authorization coverage.

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
