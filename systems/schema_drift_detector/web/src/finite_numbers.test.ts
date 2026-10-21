import {test} from "node:test";
import {strict as assert} from "node:assert";
import {detectDrift} from "./app.js";
test("nonfinite numbers are schema drift, not valid numeric records",()=>{
 const schema={amount:{type:"number"}};
 for(const value of [NaN,Infinity,-Infinity]) {
  const result=detectDrift(schema,[{amount:value}]);
  assert.equal(result.drift_detected,true);assert.deepEqual(result.type_mismatched_fields,["amount"]);
 }
 for(const value of [0,-1,2.5,null]) assert.equal(detectDrift(schema,[{amount:value}]).drift_detected,false);
 assert.equal(detectDrift(schema,[{amount:true}]).drift_detected,true);
});
