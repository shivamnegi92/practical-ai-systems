import { test } from "node:test";
import * as assert from "node:assert/strict";
import { dispatch,KnowledgeTools } from './app.js';
test('invalid message envelopes return invalid-request responses',()=>{
 const tools=new KnowledgeTools();
 for(const value of [null,[],42,'text',{}, {method:3}]) {
  const result=dispatch(value as Parameters<typeof dispatch>[0],tools) as {id:unknown,error:{code:number}};
  assert.equal(result.error.code,-32600); assert.equal(result.id,null);
 }
 const reply=dispatch({id:7,method:'tools/list'},tools) as {id:unknown};
 assert.equal(reply.id,7);
});
