import {test} from "node:test";
import {strict as assert} from "node:assert";
import {judge} from "./app.js";
test("shared vocabulary cannot compensate for contradicted numeric literals",()=>{
 for(const [claim,evidence] of [["The plan costs 80 dollars per month","The plan costs 8 dollars per month"],["The fee is 8.50 dollars","The fee is 8.05 dollars"],["Keep 30 days of history","Keep 300 days of history"]]) assert.equal(judge(claim,evidence),"unsupported");
 assert.equal(judge("The plan costs 8 dollars","The plan costs 8 dollars per month"),"supported");
 assert.equal(judge("History lasts 30 days","History lasts 30 days for 8 users"),"supported");
 assert.equal(judge("Exports support PDF","Exports support PDF"),"supported");
});
