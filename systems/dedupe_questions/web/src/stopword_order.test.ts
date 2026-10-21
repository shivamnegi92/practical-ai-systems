import {test} from "node:test";
import {strict as assert} from "node:assert";
import {tokenize} from "./app.js";
test("stopwords are removed before suffix stemming",()=>{
 assert.deepEqual(tokenize("this"),[]);
 assert.deepEqual(tokenize("THIS billing"),tokenize("billing"));
 assert.deepEqual(tokenize("this the and"),[]);
 assert.deepEqual(tokenize("thinking"),["think"]);
});
