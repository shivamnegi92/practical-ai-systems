import { test } from "node:test";
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
test("evaluation includes lexical and reduced-corpus misses", () => {
  assert.equal(evaluateAll().cases, 10);
  assert.ok(evaluateAll().recall_at_3 < 1);
});

test("synonym queries have no hits without query expansion", () => {
  const tools = new KnowledgeTools();
  for (const query of ["forgotten credentials", "paid tier price"]) assert.deepEqual(tools.search(query).results, []);
});
