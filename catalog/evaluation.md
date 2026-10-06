# Evaluation and observability

> Measure quality and inspect system behavior before and after release.

[← Back to Practical AI Systems](../README.md)

## Catalog

Records are metadata-reviewed, not blanket endorsements.

| Project | What it does | Best for | Tradeoffs to consider | Delivery | License | Evidence |
|---|---|---|---|---|---|---|
| [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) | Receive, process, and export telemetry through a vendor-neutral collector pipeline. | centralizing telemetry collection; routing traces and metrics across backends | AI-specific instrumentation, conventions, and dashboards still need to be defined. | service, platform | Apache-2.0 | metadata-reviewed |

## Choosing well

Start with the smallest component that solves the job. Validate it with your data, constraints, and failure cases before expanding the architecture.
