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
  return typeof value;
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
      if (schema[field] && value !== null && value !== "" && value !== undefined && inferType(value) !== schema[field].type) {
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

export const EVAL_CASES: Array<{ schema: Schema; records: Array<Record<string, unknown>>; gold: ReturnType<typeof detectDrift>; case_id?: string; note?: string }> = [
  {
    "schema": {
      "id": {
        "type": "number",
        "required": true
      },
      "name": {
        "type": "string",
        "required": true
      }
    },
    "records": [
      {
        "id": 1,
        "name": "A"
      },
      {
        "id": 2,
        "name": "B",
        "email": "b@x.com"
      },
      {
        "name": "C"
      },
      {
        "id": "4",
        "name": "D"
      }
    ],
    "gold": {
      "new_fields": [
        "email"
      ],
      "missing_required_fields": [
        "id"
      ],
      "type_mismatched_fields": [
        "id"
      ],
      "drift_detected": true
    }
  },
  {
    "schema": {
      "id": {
        "type": "number",
        "required": true
      },
      "name": {
        "type": "string",
        "required": true
      }
    },
    "records": [
      {
        "id": 1,
        "name": "A"
      },
      {
        "id": 2,
        "name": "B"
      }
    ],
    "gold": {
      "new_fields": [],
      "missing_required_fields": [],
      "type_mismatched_fields": [],
      "drift_detected": false
    }
  },
  {
    "case_id": "web_original",
    "schema": {
      "id": {
        "type": "number",
        "required": true
      },
      "email": {
        "type": "string",
        "required": true
      },
      "age": {
        "type": "number",
        "required": false
      }
    },
    "records": [
      {
        "id": 1,
        "email": "a@example.com",
        "age": 30
      },
      {
        "id": 2,
        "email": "b@example.com",
        "age": "thirty"
      },
      {
        "id": 3,
        "age": 25,
        "referrer": "sample"
      }
    ],
    "gold": {
      "new_fields": [
        "referrer"
      ],
      "missing_required_fields": [
        "email"
      ],
      "type_mismatched_fields": [
        "age"
      ],
      "drift_detected": true
    }
  },
  {
    "case_id": "zero_is_present",
    "schema": {
      "id": {
        "type": "number",
        "required": true
      }
    },
    "records": [
      {
        "id": 0
      }
    ],
    "gold": {
      "new_fields": [],
      "missing_required_fields": [],
      "type_mismatched_fields": [],
      "drift_detected": false
    }
  },
  {
    "case_id": "bool_is_not_number",
    "schema": {
      "count": {
        "type": "number"
      }
    },
    "records": [
      {
        "count": true
      }
    ],
    "gold": {
      "new_fields": [],
      "missing_required_fields": [],
      "type_mismatched_fields": [
        "count"
      ],
      "drift_detected": true
    }
  },
  {
    "case_id": "optional_absent",
    "schema": {
      "name": {
        "type": "string"
      }
    },
    "records": [
      {}
    ],
    "gold": {
      "new_fields": [],
      "missing_required_fields": [],
      "type_mismatched_fields": [],
      "drift_detected": false
    }
  },
  {
    "case_id": "false_is_present",
    "schema": {
      "active": {
        "type": "boolean",
        "required": true
      }
    },
    "records": [
      {
        "active": false
      }
    ],
    "gold": {
      "new_fields": [],
      "missing_required_fields": [],
      "type_mismatched_fields": [],
      "drift_detected": false
    }
  },
  {
    "case_id": "json_array",
    "schema": {
      "tags": {
        "type": "array"
      }
    },
    "records": [
      {
        "tags": [
          "a",
          "b"
        ]
      }
    ],
    "gold": {
      "new_fields": [],
      "missing_required_fields": [],
      "type_mismatched_fields": [],
      "drift_detected": false
    },
    "note": "Desired JSON container typing: a valid array should not drift. Both ports miss this."
  },
  {
    "case_id": "json_object",
    "schema": {
      "meta": {
        "type": "object"
      }
    },
    "records": [
      {
        "meta": {
          "key": "value"
        }
      }
    ],
    "gold": {
      "new_fields": [],
      "missing_required_fields": [],
      "type_mismatched_fields": [],
      "drift_detected": false
    },
    "note": "Desired JSON container typing: an object should not drift. Python calls this dict; TypeScript passes."
  },
  {
    "case_id": "array_is_not_object",
    "schema": {
      "meta": {
        "type": "object"
      }
    },
    "records": [
      {
        "meta": []
      }
    ],
    "gold": {
      "new_fields": [],
      "missing_required_fields": [],
      "type_mismatched_fields": [
        "meta"
      ],
      "drift_detected": true
    },
    "note": "An array is not a JSON object. TypeScript calls both object and misses this; Python flags it."
  }
];

export function evaluateAll() {
  const result = detectDrift(SAMPLE_SCHEMA, SAMPLE_RECORDS);
  const keys = ["new_fields", "missing_required_fields", "type_mismatched_fields", "drift_detected"] as const;
  const matched = EVAL_CASES.filter((c) => {
    const got = detectDrift(c.schema, c.records);
    return keys.every((key) => JSON.stringify(got[key]) === JSON.stringify(c.gold[key]));
  }).length;
  return { ...result, matches_expected_drift: result.drift_detected === true,
    cases: EVAL_CASES.length, exact_report_match: matched / EVAL_CASES.length };
}
