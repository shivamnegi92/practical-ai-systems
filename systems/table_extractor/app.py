"""Reconstruct a table grid from OCR line records using bounding-box clusters.

Normalizes raw OCR line+bbox records, then clusters lines into rows (by y
position) and columns (by x position) using fixed gap thresholds. OCR
itself is not run; this only works with line+bbox input.

Standalone: zero imports outside the Python standard library.
"""
from __future__ import annotations
import math


def normalize_lines(lines: list[dict]) -> list[dict]:
    """Keep only well-formed {text, bbox} records, sorted reading-order (top-to-bottom, left-to-right)."""
    out = []
    for line in lines:
        text = " ".join(str(line.get("text") if line.get("text") is not None else "").split())
        box = line.get("bbox")
        if not text or not isinstance(box, list) or len(box) != 4:
            continue
        x1, y1, x2, y2 = box
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and (not isinstance(v, float) or math.isfinite(v)) for v in box) or x2 < x1 or y2 < y1:
            continue
        out.append({"text": text, "bbox": [float(x1), float(y1), float(x2), float(y2)]})
    return sorted(out, key=lambda x: (round(x["bbox"][1], 3), x["bbox"][0]))


def _cluster(values: list[float], gap: float) -> list[list[int]]:
    """Group value indices into clusters separated by more than `gap`."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    clusters: list[list[int]] = [[order[0]]]
    for prev, idx in zip(order, order[1:]):
        if values[idx] - values[prev] > gap:
            clusters.append([])
        clusters[-1].append(idx)
    return clusters


def extract_table(lines: list[dict], row_gap: float = 5.0, col_gap: float = 40.0) -> list[list[str]]:
    normalized = normalize_lines(lines)
    if not normalized:
        return []
    row_clusters = _cluster([line["bbox"][1] for line in normalized], row_gap)
    rows = [sorted((normalized[i] for i in cluster), key=lambda c: c["bbox"][0]) for cluster in row_clusters]

    all_x = sorted({cell["bbox"][0] for row in rows for cell in row})
    col_starts = [all_x[0]]
    for x in all_x[1:]:
        if x - col_starts[-1] > col_gap:
            col_starts.append(x)

    grid = []
    for row in rows:
        cell_row = [""] * len(col_starts)
        for cell in row:
            col_index = max(i for i, start in enumerate(col_starts) if cell["bbox"][0] >= start - 1e-6)
            cell_row[col_index] = cell["text"]
        grid.append(cell_row)
    return grid
