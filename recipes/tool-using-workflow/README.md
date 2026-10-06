# Tool-using workflows: bound autonomy with explicit control

A tool-using agent is a probabilistic controller that can request actions. Treat every tool call like an external side effect: define its authority, validate its arguments, and record what happened.

## Start with a workflow, not a swarm

Write the intended steps as a normal deterministic workflow first. Mark where the next action genuinely depends on uncertain context or user intent. Let a model choose only at those decision points. A conventional state machine or queue is easier to debug when the path is known.

## A bounded architecture

```text
User goal → policy/context → model proposes action → validate + authorize
                                                  ↓                  ↓
                                              ask user          execute tool
                                                   └──── observe result ────┘
```

Separate planning from execution. The model can suggest an action; application code decides whether that action is allowed and executes it through a narrow interface.

## Minimum guardrails

- **Least privilege:** expose only the specific functions and data the task needs.
- **Typed arguments:** validate every field; reject unexpected or malformed inputs.
- **Authorization in application code:** never rely on model text to establish permission.
- **Side-effect policy:** define which actions are read-only, reversible, approval-required, or forbidden.
- **Human approval:** require confirmation before irreversible, costly, external, or sensitive actions.
- **Timeouts and limits:** cap tool duration, retries, tokens, and total action count.
- **Idempotency:** prevent duplicate actions when calls are retried.
- **Untrusted content:** treat retrieved pages/files as data, not instructions that override system policy.
- **Audit trail:** record the request, chosen tool, validated arguments, actor, outcome, and correlation ID while minimizing sensitive data.
- **Failure path:** specify when to retry, ask the user, abstain, or stop.

## Evaluation before autonomy

Create test cases for both successful and adversarial situations:

- correct tool selection and argument construction;
- missing or ambiguous user intent;
- tool timeout, partial result, and malformed response;
- duplicate/replayed requests;
- untrusted text that attempts to redirect the workflow;
- unauthorized or high-impact action;
- safe refusal and escalation to a human.

Track task success, tool-call precision, invalid-call rate, policy-violation rate, retries, latency, cost, and user correction/approval. Evaluate side effects separately from response fluency.

## When to add multi-agent structure

Only add separate agents when you can state the distinct responsibility, permissions, and measurable benefit of each. Otherwise you are multiplying handoffs and failure modes for the aesthetic pleasure of drawing more boxes.

Browse [agents and orchestration](../../catalog/agents.md), [evaluation and observability](../../catalog/evaluation.md), and [deployment and operations](../../catalog/operations.md) for candidate components. Treat a framework as an implementation choice—not a substitute for policy design and tests.
