import json
from pathlib import Path

def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.table_extractor.app import extract_table

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    cell_hits = []
    grid_hits = []
    for case in cases:
        grid = extract_table(case["lines"])
        gold = case["gold_grid"]
        grid_hits.append(grid == gold)
        flat_got = [cell for row in grid for cell in row]
        flat_gold = [cell for row in gold for cell in row]
        if len(flat_got) == len(flat_gold):
            cell_hits.extend(g == e for g, e in zip(flat_got, flat_gold))
        else:
            cell_hits.append(False)
    return {
        "documents": len(cases),
        "exact_grid_match": round(mean(grid_hits), 4),
        "cell_exact_match": round(mean(cell_hits), 4),
        "scope": "synthetic OCR line+bbox records; row/column gaps are fixed thresholds, not learned",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
