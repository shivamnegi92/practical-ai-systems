import {test} from "node:test";
import {strict as assert} from "node:assert";
import {gradeLevel,sentences} from "./app.js";
test("punctuation fragments cannot dilute readability sentence length",()=>{
 const text="The organization evaluates complex international obligations.";
 assert.equal(gradeLevel("!!! ??? ... "+text),gradeLevel(text));
 assert.equal(gradeLevel(text+" !!! ??? ..."),gradeLevel(text));
 assert.deepEqual(sentences("!!! ??? ..."),[]);
 assert.equal(gradeLevel("!!! ??? ..."),0);
 assert.deepEqual(sentences("One sentence. Another sentence!"),["One sentence.","Another sentence!"]);
});
