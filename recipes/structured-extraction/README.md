# Structured extraction: validate outputs against reality

Use model-assisted extraction when unstructured sources must become typed records—entities, fields, relationships, or events. Valid JSON is not the same as correct data. Design the schema, evidence trail, and review path before choosing a model or framework.

## Good fit

- Fields are scattered through prose, documents, or mixed layouts.
- A schema can define valid values and relationships.
- Human review can be applied to uncertain or high-impact results.

Prefer deterministic parsing or a database/API when the source is already structured and authoritative. Do not use probabilistic extraction as a substitute for access control or source-of-truth checks.

## A safe pipeline

```text
Source → parser/OCR → candidate extraction → schema validation
                                      ↓                 ↓
                                source spans       confidence/rules
                                      └──── review queue ────┘
                                                ↓
                                       accepted records
```

Preserve the original source and the text span, page, or coordinate supporting every extracted value. Keep model-generated output separate from accepted data until validation is complete.

## Design the record first

For each field, define:

- type, allowed values, and normalization rules;
- whether it is required, optional, or explicitly unknown;
- source evidence required to accept it;
- conflict-resolution rule when sources disagree;
- privacy/sensitivity classification;
- who or what can approve changes.

Represent “not present,” “ambiguous,” and “not processed” separately. A blank string should not carry three meanings and a small existential crisis.

## Validation layers

1. **Syntax:** output parses as the required format.
2. **Schema:** types, required fields, and enumerations are valid.
3. **Evidence:** every value maps to source material; citations are resolvable.
4. **Semantic rules:** cross-field constraints hold (dates, totals, identifiers, relationships).
5. **Risk-based review:** uncertain/high-impact fields go to a human; low-risk fields can use automated checks only after measuring error rates.
6. **Downstream reconciliation:** compare accepted records with an authoritative system where possible.

## Evaluate by field and failure type

Build a labeled sample that represents actual source variation. Measure field-level precision/recall, exact-match or normalized accuracy as appropriate, evidence-span correctness, invalid-schema rate, abstention, and human correction rate. Report slices by format, language, source quality, and field sensitivity. Do not hide a bad field behind a strong aggregate score.

Record the schema version, parser/OCR version, prompt or extraction code version, model identifier, temperature/configuration, and evaluation-set snapshot. Keep sensitive data out of public examples and logs.

## Common failure modes

- Plausible values appear without source evidence.
- A normalized value loses the original literal needed for audit.
- Multiple entities with the same name are merged.
- Dates, units, currencies, or locale conventions are silently changed.
- OCR/layout errors are blamed on the model.
- Schema-valid records are treated as business-valid.
- Reviewers see only the answer, not the supporting text.

Browse [information extraction and document AI](../../catalog/extraction.md) for parsing components and [evaluation and observability](../../catalog/evaluation.md) for validation/tracing tools. Evaluate the whole pipeline, not just the extraction prompt.
