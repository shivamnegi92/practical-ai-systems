import {test} from "node:test";
import {strict as assert} from "node:assert";
import {extract} from "./app.js";
test("large invoice totals are compared in exact integer cents",()=>{
 const text=(total:string)=>"Vendor: Demo\nInvoice: INV-1\nDate: 2026-01-01\nSubtotal: 1000000000000000000000000000000.00\nTax: 0.01\nTotal: "+total+"\n";
 assert.ok(extract(text("1000000000000000000000000000000.00")).errors.includes("mismatch:total"));
 assert.deepEqual(extract(text("1000000000000000000000000000000.01")).errors,[]);
});
