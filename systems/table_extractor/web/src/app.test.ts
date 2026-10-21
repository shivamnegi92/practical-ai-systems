import { normalizeLines } from "./app.js";
import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, extractTable, SAMPLE_LINES } from "./app.js";

test("reconstructs a simple 3x2 table", () => {
  const grid = extractTable(SAMPLE_LINES);
  assert.deepEqual(grid, [
    ["Name", "Qty"],
    ["Widget", "4"],
    ["Gadget", "9"],
  ]);
});

test("empty input yields empty table", () => {
  assert.deepEqual(extractTable([]), []);
});

test("malformed lines are dropped before clustering", () => {
  const grid = extractTable([{ text: "x", bbox: [0, 0, 10] } as any]);
  assert.deepEqual(grid, []);
});

test("evaluation matches the expected grid", () => {
  assert.equal(evaluateAll().matches_expected_grid, true);
});

test("normalization rejects non-finite and non-number coordinates", () => {
 for (const bad of [NaN, Infinity, -Infinity, true, false]) {
  for (let index=0; index<4; index++) {
   const box: unknown[]=[0,0,10,10]; box[index]=bad;
   assert.deepEqual(normalizeLines([{text:"bad",bbox:box}]),[]);
  }
 }
 assert.deepEqual(normalizeLines([{text:null,bbox:[0,0,1,1]}]),[]);
 assert.deepEqual(normalizeLines([{text:" ok ",bbox:[-2,-1,0,1]}]),[{text:"ok",bbox:[-2,-1,0,1]}]);
});
