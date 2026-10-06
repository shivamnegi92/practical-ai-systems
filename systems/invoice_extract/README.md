# Invoice field extraction

Extract a small invoice schema from plain text and validate amount consistency.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.invoice_extract.app systems/invoice_extract/sample.txt
```

## Evaluate and test

```bash
python3 -m systems.invoice_extract.evaluate
python3 -m unittest systems.invoice_extract.test_invoice
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

On four synthetic cases (two balanced invoices, one total mismatch, one invalid date), exact schema-field accuracy is **1.00** and validity precision/recall are **1.00/1.00**. This tiny fixture is only a smoke/regression check; it does not establish robustness to OCR, locale/currency differences, or real invoice layouts. See [`eval/results.json`](eval/results.json).

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
