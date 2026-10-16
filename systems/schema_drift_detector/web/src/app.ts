// Detect new fields, missing required fields, and type changes against a declared schema.
// Useful for catching upstream data drift before it silently breaks a
// downstream extraction or indexing pipeline.

export interface FieldSpec { type: string; required?: boolean }
export type Schema = Record<string, FieldSpec>;

function inferType(value: unknown): string {
  if (typeof value === "boolean") return "boolean";
  if (typeof value === "number") return "number";
  if (typeof value === "string") return "string";
  if (value === null || value === undefined) return "null";
  if (Array.isArray(value)) return "array";
  return typeof value;
}

function canonicalType(name: string): string {
  if (name === "list") return "array";
  if (name === "dict") return "object";
  return name;
}

export function detectDrift(schema: Schema, records: Array<Record<string, unknown>>) {
  const knownFields = new Set(Object.keys(schema));
  const required = new Set(Object.entries(schema).filter(([, spec]) => spec.required).map(([f]) => f));
  const newFields = new Set<string>();
  const missingRequired = new Set<string>();
  const typeMismatches = new Set<string>();

  for (const record of records) {
    for (const field of Object.keys(record)) if (!knownFields.has(field)) newFields.add(field);
    const present = new Set(Object.entries(record).filter(([, v]) => v !== null && v !== "" && v !== undefined).map(([k]) => k));
    for (const field of required) if (!present.has(field)) missingRequired.add(field);
    for (const [field, value] of Object.entries(record)) {
      if (schema[field] && value !== null && value !== "" && value !== undefined && canonicalType(inferType(value)) !== canonicalType(schema[field].type)) {
        typeMismatches.add(field);
      }
    }
  }

  return {
    new_fields: [...newFields].sort(),
    missing_required_fields: [...missingRequired].sort(),
    type_mismatched_fields: [...typeMismatches].sort(),
    drift_detected: newFields.size > 0 || missingRequired.size > 0 || typeMismatches.size > 0,
  };
}

export const SAMPLE_SCHEMA: Schema = {
  id: { type: "number", required: true },
  email: { type: "string", required: true },
  age: { type: "number", required: false },
};

export const SAMPLE_RECORDS: Array<Record<string, unknown>> = [
  { id: 1, email: "a@example.com", age: 30 },
  { id: 2, email: "b@example.com", age: "thirty" },
  { id: 3, age: 25, referrer: "google" },
];

export function evaluateAll() {
  const result = detectDrift(SAMPLE_SCHEMA, SAMPLE_RECORDS);
  const expectedDrift = true;
  return { ...result, matches_expected_drift: result.drift_detected === expectedDrift };
}
