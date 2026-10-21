# CSV/record schema validator

Catch missing required fields and type mismatches in structured records before they reach an AI pipeline.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.csv_schema_validator.evaluate
```

## Evaluate and test

```bash
python3 -m systems.csv_schema_validator.evaluate
python3 -m unittest systems.csv_schema_validator.test_validator
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current row-validity accuracy on a 5-row synthetic fixture covering a missing required field, a type mismatch, and two valid rows.

## Known limitations

- This checks only presence and Python type, not formats, ranges, enumerations, or cross-field business rules.
- Python's `bool` subclasses `int`, so number fields explicitly reject `true`/`false` to match the web app. Boolean fields still accept both values, and numeric zero is a valid number.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
