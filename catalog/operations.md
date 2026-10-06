# Deployment and operations

> Package, serve, scale, and operate AI workloads.

[← Back to Practical AI Systems](../README.md)

## Catalog

Records are metadata-reviewed, not blanket endorsements.

| Project | What it does | Best for | Tradeoffs to consider | Delivery | License | Evidence |
|---|---|---|---|---|---|---|
| [BentoML](https://github.com/bentoml/BentoML) | Package and serve machine-learning inference applications and APIs. | deploying model-backed services; repeatable inference packaging | Test target runtime, hardware, model compatibility, and packaging assumptions explicitly. | platform, library | Apache-2.0 | metadata-reviewed |
| [Docker Compose](https://github.com/docker/compose) | Define and run multi-container applications from a Compose configuration. | local development stacks; small services with a few cooperating containers | Useful for development and modest deployments, but not a universal production orchestrator. | tool | Apache-2.0 | metadata-reviewed |
| [Kubernetes](https://github.com/kubernetes/kubernetes) | Schedule and manage containerized workloads across clusters. | platform-scale container orchestration; standardizing deployment primitives | Can be excessive for small AI applications; include platform team and operational costs. | platform | Apache-2.0 | metadata-reviewed |
| [Ray](https://github.com/ray-project/ray) | Scale Python applications and machine-learning workloads across distributed compute. | parallel and distributed execution; workloads that exceed a single process or machine | Adds operational complexity; adopt it when distributed execution is needed, not as default ceremony. | platform, library | Apache-2.0 | metadata-reviewed |

## Choosing well

Start with the smallest component that solves the job. Validate it with your data, constraints, and failure cases before expanding the architecture.
