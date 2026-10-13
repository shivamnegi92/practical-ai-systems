# Multimodal document field pipeline

Normalize OCR line geometry and extract fields. The OCR engine itself is not tested.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.multimodal_ocr.evaluate
```

## Evaluate and test

```bash
python3 -m systems.multimodal_ocr.evaluate
python3 -m unittest systems.multimodal_ocr.test_ocr
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

Nine synthetic OCR-line records share one fixture matrix across Python and TypeScript, preserving the three original Python documents and the split-line web fixture. Empty input, invalid geometry, and whitespace/reordered lines provide controls. Two correctly labelled cases expose existing failures: the total regex matches an earlier Subtotal, and the invoice-number regex misreads the Invoice Number label.

Field exact-match is **25/27 (about 0.926)**: each document has three labelled fields, including nulls, and the score averages each document's matching-field fraction. Both failures miss one field; this is not a complete-document accuracy score. See [`eval/results.json`](eval/results.json). Extraction remains unchanged. Input is already text plus boxes; images and OCR engine accuracy are not evaluated.

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
