// Validate rows of structured data against a small declared schema.

export type FieldType = "string" | "number" | "boolean";
export interface FieldSpec { type: FieldType; required?: boolean }
export type Schema = Record<string, FieldSpec>;

function matchesType(value: unknown, type: FieldType): boolean {
  if (type === "number") return typeof value === "number" && Number.isFinite(value);
  if (type === "boolean") return typeof value === "boolean";
  return typeof value === "string";
}

export function validateRow(schema: Schema, row: Record<string, unknown>): string[] {
  const errors: string[] = [];
  for (const [field, spec] of Object.entries(schema)) {
    const value = row[field];
    if (value === undefined || value === null || value === "") {
      if (spec.required) errors.push(`missing:${field}`);
      continue;
    }
    if (!matchesType(value, spec.type)) errors.push(`type:${field}`);
  }
  return errors;
}

export function validateRows(schema: Schema, rows: Array<Record<string, unknown>>) {
  return rows.map((row, i) => ({ row: i, errors: validateRow(schema, row) }));
}

const SCHEMA: Schema = {
  id: { type: "number", required: true },
  name: { type: "string", required: true },
  active: { type: "boolean", required: false },
};

const ROWS: Array<Record<string, unknown>> = [
  { id: 1, name: "Alice", active: true },
  { id: "two", name: "Bob" },
  { name: "Carol" },
  { id: 4, name: "Dan", active: "yes" },
  { id: 5, name: "Eve" },
];
const GOLD_VALID = [true, false, false, false, true];

export function evaluateAll() {
  const results = validateRows(SCHEMA, ROWS);
  const correct = results.filter((r, i) => (r.errors.length === 0) === GOLD_VALID[i]).length;
  return { cases: ROWS.length, row_validity_accuracy: correct / ROWS.length };
}

export { SCHEMA, ROWS };
