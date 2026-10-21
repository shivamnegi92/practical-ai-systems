import { test } from "node:test";

test("invalid tool argument types produce tool errors and allow the next call", () => {
  const tools = new KnowledgeTools();
  const cases = [
    ...[null, 7, true, [], {}].map(query => ({ name: "search_docs", arguments: { query } })),
    ...[null, true, "3", 1.5, NaN, Infinity].map(limit => ({ name: "search_docs", arguments: { query: "password", limit } })),
    ...[null, 7, true, [], {}].map(chunk_id => ({ name: "read_chunk", arguments: { chunk_id } })),
  ];
  for (const params of cases) {
    const result = dispatch({ id: 4, method: "tools/call", params }, tools) as any;
    assert.equal(result.id, 4);
    assert.equal(result.result.isError, true);
    assert.equal((dispatch({ id: 5, method: "tools/list" }, tools) as any).result.tools.length, 2);
  }
  assert.deepEqual(tools.search("password", -1), tools.search("password", 1));
  assert.ok(tools.search("password").results.length > 0);
});
import { strict as assert } from "node:assert";
import { dispatch, evaluateAll, KnowledgeTools } from "./app.js";

test("tools/list returns both tools", () => {
  const response = dispatch({ method: "tools/list", id: 1 }, new KnowledgeTools());
  assert.equal((response.result as { tools: unknown[] }).tools.length, 2);
});
test("tools/call search_docs finds a relevant chunk", () => {
  const response = dispatch(
    { method: "tools/call", id: 2, params: { name: "search_docs", arguments: { query: "reset password" } } },
    new KnowledgeTools()
  );
  const content = (response.result as { content: Array<{ text: string }> }).content[0].text;
  assert.ok(content.includes("accounts.md#1"));
});
test("unknown tool returns an error", () => {
  const response = dispatch({ method: "tools/call", id: 3, params: { name: "nope", arguments: {} } }, new KnowledgeTools());
  assert.equal((response.result as { isError?: boolean }).isError, true);
});
test("unknown method returns a JSON-RPC error", () => {
  const response = dispatch({ method: "bogus", id: 4 }, new KnowledgeTools());
  assert.ok("error" in response);
});
test("evaluation recall is perfect on the bundled fixtures", () => {
  assert.equal(evaluateAll().recall_at_3, 1);
});
