import {test} from "node:test";
import {strict as assert} from "node:assert";
import {detect,redact} from "./app.js";
test("compact sixteen digit card shapes are bounded and redacted",()=>{
 assert.equal(redact("Card 4111111111111111."),"Card [REDACTED:CREDIT_CARD].");
 for(const value of ["41111111111111111","a4111111111111111","4111111111111111b"]) assert.equal(detect(value).some(x=>x.type==="credit_card"),false);
 for(const value of ["4111-1111-1111-1111","4111 1111 1111 1111"]) {
  const match=detect("Card "+value+".").find(x=>x.type==="credit_card")!;
  assert.equal(match.match,value);assert.equal(match.start,5);assert.equal(match.end,5+value.length);
 }
});
