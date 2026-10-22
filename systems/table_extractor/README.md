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

See [`eval/results.json`](eval/results.json) for ten synthetic layouts shared with the web evaluation: the two original tables, the web demonstration, empty/malformed/single/reordered/ragged controls, and two correctly labelled failures. Dense distinct columns collapse and tight distinct rows merge under the unchanged fixed gaps. Gold cells have non-overlapping boxes.

`exact_grid_match` compares full row/column shape and content per document (8/10). The legacy `cell_exact_match` is retained: equal-length flattened outputs contribute one vote per cell; a size mismatch contributes one failed vote, and empty grids contribute no cell votes. It is not a topology metric or an equally weighted document score. The web demo result fields remain available.

## Known limitations

- Row and column boundaries are fixed-gap thresholds (`row_gap`, `col_gap`), not learned from the layout; dense real tables or merged cells will break this.
- Multi-line cells and rotated text are not handled. Missing cells at known column positions are padded with blanks in the ragged-row control; this does not infer arbitrary missing columns.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
