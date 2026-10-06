# Agents and orchestration

> Build workflows that use tools, state, and human decisions.

[← Back to Practical AI Systems](../README.md)

## Catalog

Records are metadata-reviewed, not blanket endorsements.

| Project | What it does | Best for | Tradeoffs to consider | Delivery | License | Evidence |
|---|---|---|---|---|---|---|
| [AutoGen](https://github.com/microsoft/autogen) | Framework for building applications that coordinate agents, tools, and conversations. | exploring agent conversation patterns; prototyping tool-using systems | APIs and project direction can evolve; check current version guidance before starting a new implementation. | framework | MIT | metadata-reviewed |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Build agent workflows around task-oriented roles and collaboration. | prototyping role-based agent workflows; evaluating multi-agent coordination | Multiple agents can add latency, cost, and failure modes; compare against a single-agent baseline. | framework | MIT | metadata-reviewed |
| [LangGraph](https://github.com/langchain-ai/langgraph) | Orchestrate stateful agent workflows as graphs with explicit state and control flow. | workflows that need checkpoints; human approval steps; multi-step tool use | Explicit state and orchestration add design complexity; use a simpler workflow when it is enough. | framework | MIT | metadata-reviewed |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | Add AI orchestration, plugins, and memory patterns to application code. | integrating AI features into existing services; teams using multiple language ecosystems | Provider and abstraction choices should be kept explicit to avoid accidental lock-in. | sdk | MIT | metadata-reviewed |

## Choosing well

Start with the smallest component that solves the job. Validate it with your data, constraints, and failure cases before expanding the architecture.
