import {test} from "node:test";
import {strict as assert} from "node:assert";
import {checkCaption} from "./app.js";
test("word limits count word-bearing tokens, not punctuation",()=>{
 for(const text of ["!!! ??? ...","A cat !!!","-- _ ."]) assert.ok(checkCaption(text).reasons.includes("too_short"));
 assert.equal(checkCaption("Three red cars.").passed,true);
 assert.equal(checkCaption("2 red cars.").passed,true);
 assert.equal(checkCaption("Three red cars "+"! ".repeat(30)).reasons.includes("too_long"),false);
});
