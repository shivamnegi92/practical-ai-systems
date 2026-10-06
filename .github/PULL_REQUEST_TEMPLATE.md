## What changed?

- [ ] Catalog project record
- [ ] Original recipe or evaluation guide
- [ ] Catalog tooling/tests
- [ ] Other: ___

## Evidence and decision rationale

Explain what user decision this improves and link to primary sources. For catalog entries, include license and project-origin evidence; if either is unclear, move the candidate to `catalog/review-queue.json` instead of active records.

## Checklist

- [ ] Canonical source checked; duplicate ID/URL ruled out.
- [ ] Category, capabilities, and delivery modes use the controlled vocabulary.
- [ ] Description is factual and includes a meaningful tradeoff.
- [ ] Evidence level matches what was actually reviewed or tested.
- [ ] License and origin evidence are linked; origin policy passed.
- [ ] No unsupported ranking, safety, or production-readiness claims.
- [ ] Generated category pages/README index refreshed.
- [ ] `python3 -m unittest discover -s tests -v` passes.
- [ ] `python3 scripts/build_catalog.py` passes.
- [ ] `git diff --check` passes.
