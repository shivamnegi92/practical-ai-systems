import { test } from "node:test";
import * as assert from "node:assert/strict";
import { BM25 } from './app.js';
test('BM25 parameters have finite numeric domains',()=>{
 for(const k1 of [-1,NaN,Infinity,true,'1']) assert.throws(()=>new BM25({one:'orbit docs'},k1 as number));
 for(const b of [-0.1,1.1,NaN,Infinity,true,'0.5']) assert.throws(()=>new BM25({one:'orbit docs'},1.5,b as number));
 for(const b of [0,1]) {
  assert.equal(new BM25({one:'orbit docs'},0,b).search('orbit')[0][0],'one');
  assert.deepEqual(new BM25({},0,b).search('orbit'),[]);
 }
});
