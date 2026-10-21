import { test } from "node:test";
import * as assert from "node:assert/strict";
import { validateRow,validateRows, Schema } from './app.js';
test('unknown types fail before row traversal',()=>{
 for(const type of ['numbr','integer',null,[]]) {
  const schema={value:{type}} as unknown as Schema;
  assert.throws(()=>validateRow(schema,{}));
  assert.throws(()=>validateRow(schema,{value:'text'}));
  assert.throws(()=>validateRows(schema,[]));
 }
 assert.deepEqual(validateRow({a:{type:'number'},b:{type:'boolean'},c:{}} as unknown as Schema,{a:1,b:false,c:'text'}),[]);
});
