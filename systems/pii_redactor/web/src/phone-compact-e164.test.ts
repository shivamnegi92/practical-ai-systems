import { test } from "node:test";
import * as assert from "node:assert/strict";
import { detect,redact } from './app.js';
test('compact and international phone spans are complete',()=>{
 for(const value of ['5551234567','+905551234567','+442079460958','(555) 123-4567','555-123-4567']) {
  assert.deepEqual(detect('Call '+value+' now.').filter(x=>x.type==='phone').map(x=>x.match),[value]);
  assert.equal(redact('Call '+value+' now.'),'Call [REDACTED:PHONE] now.');
 }
 for(const value of ['5551234567890123','x5551234567','5551234567x','+1234567890123456']) assert.deepEqual(detect(value).filter(x=>x.type==='phone'),[]);
});
