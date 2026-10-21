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

See [`eval/results.json`](eval/results.json) for current exact-report match on 2 synthetic batches: one with a new field, a missing required field, and a type mismatch, and one clean batch.

## Known limitations

- JSON container types `array` and `object` are distinct in both implementations; legacy schema spellings `list` and `dict` are accepted as aliases. Python's `infer_type()` helper retains its existing spellings. Checks are shallow: element/property schemas, ranges, formats and semantic changes are not validated.
- Boolean values are inferred before numbers in Python, so booleans remain distinct from a declared number type.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
