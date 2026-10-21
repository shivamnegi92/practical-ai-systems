# Post-OCR table reconstruction

Cluster OCR line bounding boxes into rows and columns to rebuild a simple table grid. OCR itself is not run.

**Level:** intermediate · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.table_extractor.evaluate
```

## Evaluate and test

```bash
python3 -m systems.table_extractor.evaluate
python3 -m unittest systems.table_extractor.test_extractor
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json) for current cell-level exact match on 2 synthetic 2x3 table fixtures, one with clean rows and one with small intra-row y jitter.

## Known limitations

- Row and column boundaries are fixed-gap thresholds (`row_gap`, `col_gap`), not learned from the layout; dense real tables or merged cells will break this.
- Multi-line cells, rotated text, and ragged column counts across rows are not handled.
- Fragments assigned to the same row and column are joined with spaces in left-to-right order instead of overwriting earlier text. This preserves text but does not infer merged cells or recover cell boundaries that the fixed-gap clustering missed.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
