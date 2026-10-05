# Repository guidance for AI coding agents

- This repository is a curated directory/catalog of practical AI systems, not a monolith or an automatic mirror of other catalogs.
- Use `.claude/skills/practical-ai-systems-trend-curator/SKILL.md` when discovering current/trending repositories or refreshing the catalog. This is a project-local Claude Code skill: invoke `/practical-ai-systems-trend-curator weekly`, `monthly`, or `audit` from Claude Code in this repository. Other agents should read the skill file and follow its workflow.
- Read `CONTRIBUTING.md` before adding a project. Preserve the catalog's origin policy, verify current source evidence, and distinguish reviewed, tested, and merely linked items.
- Never bulk-copy project entries or prose from Shubham Saboo, Nir Diamant, or other upstream repositories. Link and attribute canonical sources.
- Never infer project origin from a person's name or nationality. Hold ambiguous cases for review.
- Do not modify unrelated user work. Check `git status` and inspect diffs before editing.
- The trend curator is allowed to create local catalog updates only when checks pass. It must not commit, push, publish, or open PRs without explicit separate instruction.
- Run `python3 -m unittest discover -s tests -v` and `python3 scripts/catalog_update.py` after changes to the managed trend section.
