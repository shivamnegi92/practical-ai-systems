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

On three synthetic OCR-line records with supplied bounding boxes, field exact-match is **1.00**. The OCR engine and image understanding are not run or evaluated here—the input is already OCR text plus boxes. This is a post-OCR parsing fixture only. See [`eval/results.json`](eval/results.json).

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
