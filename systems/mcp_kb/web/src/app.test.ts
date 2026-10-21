import { test } from "node:test";
import { strict as assert } from "node:assert";
import { dispatch, evaluateAll, KnowledgeTools } from "./app.js";

test("named tools/call params reject non-objects with a correlated error", () => {
  const tools=new KnowledgeTools();
  for (const params of [null,[],["read_chunk"],"bad",7,true]) {
    const message=JSON.parse(JSON.stringify({id:"bad-call",method:"tools/call",params}));
    assert.deepEqual(dispatch(message,tools),{jsonrpc:"2.0",id:"bad-call",error:{code:-32602,message:"params must be an object"}});
  }
  const valid=dispatch({id:1,method:"tools/call",params:{name:"read_chunk",arguments:{chunk_id:"accounts.md#1"}}},tools);
  assert.equal((valid.result as {isError?:boolean}).isError,undefined);
});

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
