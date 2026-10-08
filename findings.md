# Practical AI Systems — product notes

## Core idea

Build original AI-system examples that are runnable and evaluated. Each project should show the task, implementation, evaluation cases, measured outcome, and failure modes so learners can understand not just how to make a demo, but how to inspect one.

## Current baseline

- 10 runnable prototypes in `systems/`.
- 20 external projects in a separate structured toolbox spanning six categories.
- Shared offline helpers for retrieval, metrics, and optional model providers.
- CI validates generated views, tests, evaluation packets, and examples.
- README onboarding targets first-timers, students/instructors, and professional builders.

## Current constraints

- The examples and evaluations are intentionally small; scores only describe the committed synthetic fixtures.
- OCR is not included in the post-OCR example; the input is already text and bounding boxes.
- Voice-call latency is fixture metadata, not measured runtime latency.
- The MCP example is a minimal illustrative subset, not a client-conformance claim.
- The repository should not claim production readiness, security certification, or broad model quality from these prototypes.

## Direction

Make project pages feel like short practical labs: run, modify one thing, evaluate, inspect the failure, and explain the trade-off. Add breadth only when there is enough time to maintain each project to that standard.
