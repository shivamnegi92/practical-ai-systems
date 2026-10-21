import { test } from "node:test";
import { strict as assert } from "node:assert";
import { evaluateAll, extractTable, SAMPLE_LINES } from "./app.js";

test("keeps all fragments in one cell in left-to-right order", () => {
  assert.deepEqual(extractTable([
    { text: "York", bbox: [20, 0, 30, 8] },
    { text: "2", bbox: [100, 0, 110, 8] },
    { text: "New", bbox: [0, 0, 10, 8] },
    { text: "Los", bbox: [0, 20, 10, 28] },
    { text: "Angeles", bbox: [20, 20, 30, 28] },
  ]), [["New York", "2"], ["Los Angeles", ""]]);
  assert.deepEqual(extractTable([
    { text: "ha", bbox: [0, 0, 10, 8] },
    { text: "ha", bbox: [20, 0, 30, 8] },
  ]), [["ha ha"]]);
});

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
