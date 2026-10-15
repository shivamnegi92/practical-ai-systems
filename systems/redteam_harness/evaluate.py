import json
from pathlib import Path

from systems.redteam_harness.app import build_agent, run_battery

EVAL_DIR = Path(__file__).parent / "eval"


def evaluate():
    cases = json.loads((EVAL_DIR / "cases.json").read_text())
    report = run_battery(build_agent(), cases)
    return {
        "cases": report["cases"],
        "breach_rate": report["breach_rate"],
        "scope": "fourteen synthetic policy requests against one allow-list/approval policy; not an exhaustive attack surface",
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
