# Schema drift detector

Diff a batch of records against a declared schema: new fields, missing required fields, and type mismatches.

**Level:** intermediate · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.schema_drift_detector.evaluate
```

## Evaluate and test

```bash
python3 -m systems.schema_drift_detector.evaluate
python3 -m unittest systems.schema_drift_detector.test_drift
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

The canonical matrix now contains 10 synthetic batches, preserving the original two and adding a web-style batch, zero/false/optional-field controls, and JSON container cases. Both ports score **8/10** exact reports on the same matrix, but fail different cases. See [`eval/results.json`](eval/results.json); the existing web demonstration remains available alongside the matrix score.

## Known limitations

- This only compares field presence and Python-inferred type; it has no notion of value ranges, formats, enumerations, or semantic meaning changes.
- Boolean values are explicitly classified before numbers; the new `bool_is_not_number` control confirms that a declared number rejects `true`.
- The container gold labels use JSON semantic types, a desired expectation beyond the primitive baseline: an array is not an object. Python calls containers `list`/`dict`, incorrectly flagging valid declared `array`/`object` values. TypeScript calls arrays `object`, incorrectly flagging declared arrays and missing an array passed to an object field. These limitations are kept in the evaluation; inference is unchanged.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
