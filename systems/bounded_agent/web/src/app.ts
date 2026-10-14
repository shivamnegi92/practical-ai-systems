// A deterministic, allow-listed workflow with explicit human approval.

export interface Plan {
  action: string;
  arguments: Record<string, unknown>;
  requiresApproval: boolean;
}

export class BoundedAgent {
  constructor(
    private tools: Record<string, (args: Record<string, unknown>) => unknown>,
    private allowed: Set<string>,
    private approvalRequired: Set<string> = new Set()
  ) {
    if (approvalRequired.size === 0) this.approvalRequired = new Set(allowed);
  }

  plan(request: { action?: string; arguments?: unknown }): Plan {
    const action = request.action ?? "";
    if (!this.allowed.has(action) || !(action in this.tools)) throw new Error("action is not allow-listed");
    const args = request.arguments ?? {};
    if (typeof args !== "object" || args === null || Array.isArray(args)) throw new Error("arguments must be an object");
    return { action, arguments: args as Record<string, unknown>, requiresApproval: this.approvalRequired.has(action) };
  }

  run(plan: Plan, approved = false) {
    if (!this.allowed.has(plan.action) || !(plan.action in this.tools)) throw new Error("action is not allow-listed");
    if (typeof plan.arguments !== "object" || plan.arguments === null) throw new Error("arguments must be an object");
    if (plan.requiresApproval && !approved) return { status: "awaiting_approval", action: plan.action };
    return { status: "completed", action: plan.action, result: this.tools[plan.action](plan.arguments) };
  }
}

export function buildSampleAgent(): BoundedAgent {
  const tools = {
    lookup_order: (args: Record<string, unknown>) => ({ order_id: args.order_id }),
    send_refund: (args: Record<string, unknown>) => ({ queued: args.amount }),
  };
  return new BoundedAgent(tools, new Set(["lookup_order", "send_refund"]), new Set(["send_refund"]));
}

function evaluateDemo() {
  const agent = buildSampleAgent();
  const lookupPlan = agent.plan({ action: "lookup_order", arguments: { order_id: "A1" } });
  const lookupResult = agent.run(lookupPlan);
  const refundPlan = agent.plan({ action: "send_refund", arguments: { amount: 10 } });
  const unapproved = agent.run(refundPlan, false);
  const approved = agent.run(refundPlan, true);
  let rejected = false;
  try {
    agent.plan({ action: "delete_account", arguments: {} });
  } catch {
    rejected = true;
  }
  return {
    lookup_completes_without_approval: lookupResult.status === "completed",
    refund_awaits_approval: unapproved.status === "awaiting_approval",
    refund_completes_once_approved: approved.status === "completed",
    disallowed_action_rejected: rejected,
  };
}

export interface EvalCase {
  name?: string;
  request: { action?: string; arguments?: unknown };
  approved: boolean;
  expected: string;
}
export const EVAL_CASES: EvalCase[] = [
  {
    "request": {
      "action": "lookup_order",
      "arguments": {
        "order_id": "A-1"
      }
    },
    "approved": true,
    "expected": "completed"
  },
  {
    "request": {
      "action": "send_refund",
      "arguments": {
        "amount": 900
      }
    },
    "approved": false,
    "expected": "awaiting_approval"
  },
  {
    "request": {
      "action": "delete_account",
      "arguments": {}
    },
    "approved": true,
    "expected": "rejected"
  },
  {
    "name": "web lookup without approval",
    "request": {
      "action": "lookup_order",
      "arguments": {
        "order_id": "A1"
      }
    },
    "approved": false,
    "expected": "completed"
  },
  {
    "name": "web refund awaits approval",
    "request": {
      "action": "send_refund",
      "arguments": {
        "amount": 10
      }
    },
    "approved": false,
    "expected": "awaiting_approval"
  },
  {
    "name": "web refund approved",
    "request": {
      "action": "send_refund",
      "arguments": {
        "amount": 10
      }
    },
    "approved": true,
    "expected": "completed"
  },
  {
    "name": "array arguments refused",
    "request": {
      "action": "lookup_order",
      "arguments": []
    },
    "approved": true,
    "expected": "rejected"
  },
  {
    "name": "unknown export refused",
    "request": {
      "action": "export_customers",
      "arguments": {}
    },
    "approved": true,
    "expected": "rejected"
  },
  {
    "name": "malformed refund arguments refused",
    "request": {
      "action": "send_refund",
      "arguments": "amount=10"
    },
    "approved": true,
    "expected": "rejected"
  },
  {
    "name": "approval does not allow delete",
    "request": {
      "action": "delete_account",
      "arguments": {}
    },
    "approved": false,
    "expected": "rejected"
  }
];
export function evaluateAll() {
  const agent = buildSampleAgent();
  let passed = 0;
  for (const item of EVAL_CASES) {
    let status: string;
    try { status = agent.run(agent.plan(item.request), item.approved).status; }
    catch (error) {
      if (!(error instanceof Error) || !["action is not allow-listed", "arguments must be an object"].includes(error.message)) throw error;
      status = "rejected";
    }
    if (status === item.expected) passed++;
  }
  return {...evaluateDemo(), cases: EVAL_CASES.length, policy_cases_passed: passed,
    policy_accuracy: passed / EVAL_CASES.length};
}
