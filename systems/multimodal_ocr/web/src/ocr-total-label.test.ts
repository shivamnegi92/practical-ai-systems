import { test } from "node:test";
import * as assert from "node:assert/strict";
import { extractFields } from './app.js';
test('subtotal cannot provide a total',()=>{
 const line=(text:string,y=0)=>({text,bbox:[0,y,10,y+10] as [number,number,number,number]});
 assert.equal(extractFields([line('Subtotal: $12.00')]).total,null);
 assert.equal(extractFields([line('Subtotal: $12.00'),line('Total: $15.00',20)]).total,'15.00');
 assert.equal(extractFields([line('Grand Total: $15.00')]).total,'15.00');
});
