# PII pattern redactor

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

Seven synthetic fixtures retain the original five and add two correctly labelled known phone misses: `+44 20 7946 0958` and `5551234567`. With detection unchanged, precision is **1.0**, recall **0.6667**, and F1 **0.8** (4 true-positive types, 0 false-positive types, 2 false-negative types). See [`eval/results.json`](eval/results.json). The web evaluation uses the same seven inputs and labels.

## Known limitations

- The current phone pattern covers formatted North American-style numbers, not these international spaced or ten-bare-digit inputs. Both survive redaction unchanged, so a clean result does not establish absence of phone data. The evaluation counts detected types per case, not individual spans or completeness of redaction; the two misses are separate cases to avoid one detected phone hiding another missed phone.

- This is regex pattern matching, not a trained PII/NER model and not a compliance or security tool. It will miss anything that does not match these four shapes (addresses, names, international formats, etc.).
- Patterns can false-positive on lookalike numbers. Review every match before using this for real redaction.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
