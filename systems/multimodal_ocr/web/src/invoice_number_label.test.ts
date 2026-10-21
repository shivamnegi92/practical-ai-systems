import {test} from "node:test";
import {strict as assert} from "node:assert";
import {extractFields} from "./app.js";
const fields=(text:string)=>extractFields([{text,bbox:[0,0,100,10]}]);
test("invoice identifiers require an explicit number label",()=>{
 for(const text of ["Invoice Date: 2026-01-01","Invoice Total: $4.00","Invoice","Preinvoice: INV-7"]) assert.equal(fields(text).invoice_number,null);
 for(const text of ["Invoice Number: INV-7","Invoice No. INV-7","Invoice # INV-7","Invoice: INV-7"]) assert.equal(fields(text).invoice_number,"INV-7");
});
