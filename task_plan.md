# Practical AI Systems — product plan

_Last updated: 2026-10-07_

## Product idea

**Practical AI Systems is an original collection of runnable AI systems, each paired with an evaluation, failure cases, and implementation trade-offs.** The distinctive promise is that builders can run a system, inspect how it behaves, and see what the evaluation does and does not establish.

This repository is not a ranking, endorsement, or mirror of other collections. The curated catalog is a secondary toolbox; the original systems and their learning value are the product.

## Current inventory

- 10 offline-first runnable system prototypes under `systems/`.
- Each system includes a quickstart, code, small synthetic evaluation fixtures, a recorded result, and stated limitations.
- Shared provider, text, and metric helpers live in `common/`.
- The README has entry points for first-timers, students, instructors, and professional teams, with Beginner / Intermediate / Advanced project levels.
- The structured toolbox contains 20 reviewed external projects in six topic areas. These are clearly identified as external projects.

Current quality boundary: the examples are learning prototypes, not production services. Small synthetic-fixture scores are regression checks, not general performance claims. No system requires a model download or paid API to run its baseline.

## Product principles

1. **Run before reading a wall of theory.** Every system should have a short, working quickstart.
2. **Measure the task, not the demo.** Show the evaluation cases, metric, sample count, method, and limitations.
3. **Make failures visible.** Include adversarial, unanswerable, invalid, or unsafe cases where relevant.
4. **Progress by prerequisite.** Beginner, Intermediate, and Advanced describe the skills needed to learn from a project—not its quality.
5. **One system, one coherent job.** Avoid shallow wrappers and examples that exist only to increase the count.
6. **Keep first-run friction low.** Offline baselines and tests must not need secrets, paid services, or network access.
7. **Attribute external material.** Original code and writing must be distinguishable from linked projects and third-party material.
8. **Protect user trust.** No unsupported safety, production-readiness, ranking, or performance claims.

## Roadmap

### Phase 1 — First 10 systems (prototype set in place; quality polish remains)
- [x] Build first-pass examples spanning retrieval, extraction, agents, evaluation, and operations.
- [x] Give each example its own code, synthetic cases, result packet, and focused tests.
- [x] Add shared offline evaluation and CI checks.
- [ ] Review each README for one-command-first usability, prerequisites, and a clear “when not to use this.”
- [ ] Expand thin evaluation sets with more edge cases and independently reviewed labels.
- [ ] Add a fresh-clone smoke-test job to CI.

### Phase 2 — Flagship tutorials and runnable depth
- [ ] Turn the strongest systems into full tutorials: problem, architecture, baseline, setup, experiment, result interpretation, failure analysis, and extension exercise.
- [ ] Prioritize original work in document AI, structured/entity extraction, and voice-system evaluation.
- [ ] Record real latency/cost only when actually measured under documented conditions; otherwise say “not measured.”
- [ ] Add optional model-backed variants only where they teach something the deterministic baseline cannot.

### Phase 3 — Learning and contribution loop
- [ ] Add course-style paths with prerequisites and numbered checkpoints where appropriate.
- [ ] Add reproducible project templates, issue forms, good-first-contribution tasks, and contributor credit.
- [ ] Publish a changelog and releases only when the release checklist is met.
- [ ] Schedule a read-only freshness report for external links and dependency changes.

### Phase 4 — Scale by demonstrated usefulness
- [ ] Grow toward 30 then 50 systems only if each addition meets the same run/eval/failure-mode bar.
- [ ] Add a generated docs site only if learners need navigation that GitHub Markdown cannot provide.
- [ ] Add cross-system comparisons only when methods, versions, datasets, and conditions are genuinely comparable.
- [ ] Use reader issues, pull requests, and usage signals to choose the next systems; do not optimize for vanity counts.

## Acceptance bar for a new system

- Fresh-clone quickstart is short and succeeds as documented.
- Offline unit tests pass; default path needs no credentials or external service.
- Evaluation input, method, case count, metrics, and result packet are reproducible.
- At least one meaningful failure/negative case is included where applicable.
- README states prerequisites, scope, limitations, and when not to use the example.
- Code/data provenance and licensing are clear; no confidential or sensitive data.

## Immediate next actions

1. Polish the first-run path and Beginner / Intermediate / Advanced sections in `/Users/s0n0611/Documents/GitHub/practical-ai-systems/README.md`.
2. Review each of the ten system READMEs against the acceptance bar.
3. Strengthen the smallest synthetic evaluations, beginning with voice safety and judge-agreement cases.
4. Add fresh-clone validation before expanding the project count.
