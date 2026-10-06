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

## Risks to manage
- Generated path metadata may refer to missing project IDs or files: fail validation in unit tests.
- More project entries without maintenance capacity create stale confidence: don't expand catalog breadth in this slice.
- Evidence level can be mistaken for endorsement: keep explicit caveats.
- Popularity metrics are volatile and should not drive quality decisions.
- Held items stay held until license/origin/activity checks meet policy.
