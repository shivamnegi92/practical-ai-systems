import { test } from "node:test";
import { strict as assert } from "node:assert";
import { score } from "./app.js";
test("span scores distinguish wrong and repeated positions", () => {
 const first = {text:"Jane Doe",type:"PERSON" as const,start:0,end:8};
 const second = {...first,start:20,end:28};
 assert.equal(score([second],[first]).f1,0);
 assert.equal(score([first],[first,second]).recall,0.5);
 assert.equal(score([first,first],[first]).f1,1);
});
