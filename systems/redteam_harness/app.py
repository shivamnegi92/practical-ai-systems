"""Red-team a BoundedAgent-style policy with adversarial requests and measure the breach rate.

Carries its own copy of the allow-list/approval policy (see
`systems/bounded_agent` for the original, standalone version of this
pattern) and throws a battery of disallowed actions, unapproved sensitive
actions, malformed arguments, and an injection-style argument payload at it.

Standalone: zero imports outside the Python standard library.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Plan:
    action: str
    arguments: dict
    requires_approval: bool


class BoundedAgent:
    def __init__(self, tools: dict[str, Callable], allowed: set[str], approval_required: set[str] | None = None):
        self.tools, self.allowed = tools, allowed
        self.approval_required = approval_required or set(allowed)

    def plan(self, request: dict) -> Plan:
        action = request.get("action", "")
        if action not in self.allowed or action not in self.tools or not callable(self.tools[action]):
            raise ValueError("action is not allow-listed")
        args = request.get("arguments", {})
        if not isinstance(args, dict):
            raise ValueError("arguments must be an object")
        return Plan(action, args, action in self.approval_required)

    def run(self, plan: Plan, approved: bool = False):
        if plan.action not in self.allowed or plan.action not in self.tools or not callable(self.tools[plan.action]):
            raise ValueError("action is not allow-listed")
        if not isinstance(plan.arguments, dict):
            raise ValueError("arguments must be an object")
        if plan.requires_approval and not approved:
            return {"status": "awaiting_approval", "action": plan.action}
        return {"status": "completed", "action": plan.action, "result": self.tools[plan.action](**plan.arguments)}


def build_agent() -> BoundedAgent:
    tools = {
        "lookup_order": lambda order_id: {"order_id": order_id},
        "send_refund": lambda amount: {"queued": amount},
    }
    return BoundedAgent(tools, {"lookup_order", "send_refund"}, approval_required={"send_refund"})


def run_battery(agent: BoundedAgent, cases: list[dict]) -> dict:
    results = []
    for case in cases:
        try:
            plan = agent.plan(case["request"])
            outcome = agent.run(plan, case.get("approved", False))["status"]
        except ValueError:
            outcome = "rejected"
        breach = outcome == "completed" and not case["should_be_allowed"]
        results.append({"name": case["name"], "outcome": outcome, "breach": breach})
    breach_rate = sum(r["breach"] for r in results) / len(results) if results else 0.0
    return {"cases": len(results), "breach_rate": breach_rate, "results": results}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("cases_file", type=Path)
    args = parser.parse_args()
    cases = json.loads(args.cases_file.read_text())
    print(json.dumps(run_battery(build_agent(), cases), indent=2))


if __name__ == "__main__":
    main()
