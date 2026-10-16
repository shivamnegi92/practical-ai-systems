# PII pattern redactor

Redaction merges overlapping detected spans before replacing text. The earliest-starting match supplies the tag (longest match wins a shared start), so an SSN-shaped substring inside an email does not corrupt the email replacement or surrounding text. `detect()` still reports each original finding. This does not expand the toy pattern coverage or establish compliance.

Find and mask obvious email, phone, SSN, and credit-card-shaped strings in free text.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.pii_redactor.app "Contact jane.doe@example.com or call (555) 123-4567."
```

## Evaluate and test

```bash
python3 -m systems.pii_redactor.evaluate
python3 -m unittest systems.pii_redactor.test_redactor
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current precision/recall on 5 synthetic fixtures covering one example of each pattern plus a clean-text case.

## Known limitations

- This is regex pattern matching, not a trained PII/NER model and not a compliance or security tool. It will miss anything that does not match these four shapes (addresses, names, international formats, etc.).
- Patterns can false-positive on lookalike numbers. Review every match before using this for real redaction.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
