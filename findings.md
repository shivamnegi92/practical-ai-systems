# Findings — 10× repo improvement

## Baseline
- Public repo: https://github.com/shivamnegi92/practical-ai-systems
- Current main: `1b3e212` (catalog field guide), clean working tree at start.
- Current inventory: structured projects, six category views, three original recipes, benchmark guidance, tested lexical retrieval baseline, metadata renderer/tests, CI.
- Active catalog: 20 projects; hold queue: 7 candidates.
- Current tests: 19 catalog/site + 4 lexical-example tests in last verified run.

## Reference patterns researched (2026-10-05)
- `Shubhamsaboo/awesome-llm-apps`: use-case categories, starter-to-advanced progression, runnable app examples, CI and frequent maintenance.
- `NirDiamant/agents-towards-production`: lifecycle taxonomy, specific contribution/tutorial contract, production concerns, citation and agent docs.
- `NirDiamant/RAG_Techniques`: per-technique explanation + notebook/script + evaluation/tests/data/assets separation.
- `roadmap.sh/developer-roadmap`: path-based visual navigation and generated/productized views over structured content.
- `GokuMohandas/Made-With-ML`: coherent Design → Develop → Deploy → Iterate learning path, executable code/tests/deployment and docs-site pairing.

## Strategic synthesis
The repo has a reasonable catalog and operations baseline; its next best leverage is experience orchestration: give visitors concrete routes through existing assets before adding many more entries. Phase 1 therefore generates paths using existing project IDs, recipes, and the lexical baseline; it does not duplicate their prose or claim performance results.

## Live snapshot of top repos (GitHub API, 2026-10-05)

| Repo | Stars | Forks | Created | Contributors | Shape |
|---|---:|---:|---|---:|---|
| codecrafters-io/build-your-own-x | 551.7k | 51.8k | 2018-05 | - | Single curated list, one strong promise |
| donnemartin/system-design-primer | 373.3k | 58.8k | 2017-02 | - | Deep original guide + diagrams + Anki |
| Shubhamsaboo/awesome-llm-apps | 140.8k | 20.7k | 2024-04 | ~118 | 100+ runnable app folders, starter/advanced, wave folders (mcp, agent_skills, voice, generative_ui) |
| microsoft/generative-ai-for-beginners | 121.0k | 63.7k | 2023-06 | ~157 | 21 numbered lessons, devcontainer, translations (fork-heavy) |
| rasbt/LLMs-from-scratch | 106.1k | 16.3k | 2023-07 | ~73 | Book companion, chapter folders, tests, CITATION.cff |
| mlabonne/llm-course | 83.3k | 9.7k | 2023-06 | ~3 | README-only roadmap + Colab links; distribution via X/HF/blog/book |
| dair-ai/Prompt-Engineering-Guide | 78.8k | 8.7k | 2022-12 | - | Guide + docs site |
| microsoft/ai-agents-for-beginners | 76.5k | 25.1k | 2024-11 | ~108 | 18 numbered lessons |
| GokuMohandas/Made-With-ML | 49.7k | 7.8k | 2018-11 | - | Lifecycle course, code + tests + docs site |
| e2b-dev/awesome-ai-agents | 30.3k | 3.6k | 2023-06 | - | Curated list |
| NirDiamant/RAG_Techniques | 29.7k | 3.6k | 2024-07 | ~47 | 42+ notebooks + runnable scripts, eval/, tests/, AGENTS.md, CITATION.cff, llms.txt; 18 topics |
| NirDiamant/GenAI_Agents | 24.5k | 4.1k | 2024-09 | - | 50+ agent tutorials; 19 topics |
| NirDiamant/agents-towards-production | 21.5k | 2.9k | 2025-06 | ~27 | Production tutorials; ~21.5k stars in ~16 months |
| shivamnegi92/practical-ai-systems | 0 | 0 | 2026-10 | 1 | 20 linked projects, 3 recipes, 1 example; no description/topics/homepage |

Key takeaways: winners ship countable original runnable units with one template, visible progression, fast topic-wave coverage, and heavy author distribution. Curated link lists only win when they are first or definitive in a category; that slot is taken for general LLM apps. Full plan: `task_plan.md`.
