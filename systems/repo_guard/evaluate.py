"""Evaluate the public scanner on isolated synthetic files."""
import json
import tempfile
from pathlib import Path

from systems.repo_guard.app import scan


def evaluate():
    rows = json.loads((Path(__file__).parent / 'eval' / 'cases.json').read_text())
    tp = fp = fn = 0
    for row in rows:
        relative = Path(row['path'])
        if relative.anchor or '..' in relative.parts:
            raise ValueError('fixture path must stay inside the temporary repository')
        # One repository per row keeps repeated fixture paths independent.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(row['text'], encoding='utf-8')
            found = bool(scan(root))
        expected = row['findings'] > 0
        tp += found and expected
        fp += found and not expected
        fn += not found and expected
    return {
        'cases': len(rows),
        'recall': tp / (tp + fn) if tp + fn else 0,
        'precision': tp / (tp + fp) if tp + fp else 0,
        'scope': 'file-level finding presence through the public scanner; toy patterns, not a security scanner',
    }


if __name__ == '__main__':
    print(json.dumps(evaluate(), indent=2))
