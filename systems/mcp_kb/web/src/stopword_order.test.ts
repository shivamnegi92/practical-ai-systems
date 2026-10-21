import {test} from "node:test";
import {strict as assert} from "node:assert";
import {CHUNKS,KnowledgeTools} from "./app.js";
test("stopword-only queries cannot retrieve a stopword-only document",()=>{
 CHUNKS["stopword-test"]="this";
 try { assert.deepEqual(new KnowledgeTools().search("this").results,[]); }
 finally { delete CHUNKS["stopword-test"]; }
});
