// Reconstruct a table grid from OCR line records using bounding-box clusters.
// Clusters lines into rows (by y position) and columns (by x position) using
// fixed gap thresholds. OCR itself is not run; only line+bbox input works.

export interface OcrLine { text: string; bbox: [number, number, number, number] }

export function normalizeLines(lines: Array<{ text?: unknown; bbox?: unknown }>): OcrLine[] {
  const out: OcrLine[] = [];
  for (const line of lines) {
    const text = String(line.text ?? "").split(/\s+/).filter(Boolean).join(" ");
    const box = line.bbox;
    if (!text || !Array.isArray(box) || box.length !== 4) continue;
    const [x1, y1, x2, y2] = box;
    if (!box.every((v) => typeof v === "number") || x2 < x1 || y2 < y1) continue;
    out.push({ text, bbox: [x1, y1, x2, y2] });
  }
  return out.sort((a, b) => Math.round(a.bbox[1] * 1000) - Math.round(b.bbox[1] * 1000) || a.bbox[0] - b.bbox[0]);
}

function cluster(values: number[], gap: number): number[][] {
  const order = [...values.keys()].sort((a, b) => values[a] - values[b]);
  const clusters: number[][] = [[order[0]]];
  for (let i = 1; i < order.length; i++) {
    if (values[order[i]] - values[order[i - 1]] > gap) clusters.push([]);
    clusters[clusters.length - 1].push(order[i]);
  }
  return clusters;
}

export function extractTable(
  lines: Array<{ text?: unknown; bbox?: unknown }>,
  rowGap = 5.0,
  colGap = 40.0
): string[][] {
  const normalized = normalizeLines(lines);
  if (!normalized.length) return [];
  const rowClusters = cluster(normalized.map((l) => l.bbox[1]), rowGap);
  const rows = rowClusters.map((idxs) => idxs.map((i) => normalized[i]).sort((a, b) => a.bbox[0] - b.bbox[0]));

  const allX = [...new Set(rows.flat().map((c) => c.bbox[0]))].sort((a, b) => a - b);
  const colStarts = [allX[0]];
  for (const x of allX.slice(1)) {
    if (x - colStarts[colStarts.length - 1] > colGap) colStarts.push(x);
  }

  return rows.map((row) => {
    const cellRow = new Array(colStarts.length).fill("");
    for (const cell of row) {
      let colIndex = 0;
      for (let i = 0; i < colStarts.length; i++) if (cell.bbox[0] >= colStarts[i] - 1e-6) colIndex = i;
      cellRow[colIndex] = [cellRow[colIndex], cell.text].filter(Boolean).join(" ");
    }
    return cellRow;
  });
}

export const SAMPLE_LINES: Array<{ text: string; bbox: [number, number, number, number] }> = [
  { text: "Name", bbox: [0, 0, 50, 10] },
  { text: "Qty", bbox: [100, 0, 130, 10] },
  { text: "Widget", bbox: [0, 20, 50, 30] },
  { text: "4", bbox: [100, 20, 110, 30] },
  { text: "Gadget", bbox: [0, 40, 50, 50] },
  { text: "9", bbox: [100, 40, 110, 50] },
];

export function evaluateAll() {
  const grid = extractTable(SAMPLE_LINES);
  const expected = [
    ["Name", "Qty"],
    ["Widget", "4"],
    ["Gadget", "9"],
  ];
  const matches = JSON.stringify(grid) === JSON.stringify(expected);
  return { rows: grid.length, cols: grid[0]?.length ?? 0, matches_expected_grid: matches };
}
