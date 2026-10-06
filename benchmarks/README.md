# Evaluation playbook

A benchmark is a measurement instrument, not a leaderboard-shaped decoration. Start from a user task and its failure costs; define what evidence would change an engineering decision.

## A reproducible evaluation record

For every reported result, record:

| Field | What to capture |
|---|---|
| Task | User goal and success/failure definition |
| Dataset | Source, license/permissions, version, sample size, and split method |
| System | Code revision, component versions, configuration, and prompt/schema versions |
| Runtime | Hardware, service/model version, region if relevant, load, and time window |
| Metrics | Formula, aggregation, confidence interval or uncertainty where useful |
| Baseline | Existing system or simpler alternative measured under the same conditions |
| Provenance | Upstream-reported, locally smoke-tested, or independently reproduced |
| Limitations | Known gaps, excluded cases, and threats to validity |

Never mix results from different corpus snapshots or metric definitions without making that distinction visible.

## Choose metrics from failure costs

- Retrieval: recall@k, precision@k, ranking quality, access-control correctness.
- Extraction: field-level correctness, source-span support, invalid output, abstention, correction rate.
- Agents: task success, valid tool calls, unauthorized side effects, recovery, escalation quality.
- Multimodal pipelines: quality by media/source condition, parsing failures, latency, and cost.
- Operations: availability, latency distributions, throughput, resource use, and failure recovery.

A fluent answer, valid schema, or passing smoke test is not end-to-end task success.

## Minimal protocol

1. Define intended users and decisions the evaluation should inform.
2. Sample representative normal, edge, ambiguous, and unanswerable cases.
3. Label a small trusted set with documented adjudication rules.
4. Run a simple baseline and the candidate with identical inputs/conditions.
5. Inspect errors qualitatively; map each to a component and impact.
6. Report slices and uncertainty, not only one aggregate.
7. Repeat after changes and preserve the previous run for comparison.

## Report template

Copy this template into a dated evaluation report:

```text
Title / date:
Decision this evaluation informs:
Task + success criteria:
Dataset/source + version + permissions:
Systems + code/config versions:
Runtime conditions:
Metrics + definitions:
Baseline and candidate results:
Error analysis / slices:
Reproduction instructions:
Evidence level: upstream-reported | smoke-tested | independently-tested
Limitations and next decision:
```

## Current benchmark status

This repository currently provides evaluation guidance, **not an independently run comparative benchmark**. The catalog does not rank its listed projects. Future comparisons should be added only with a published protocol, reproducible inputs, equivalent conditions, and clear provenance.
