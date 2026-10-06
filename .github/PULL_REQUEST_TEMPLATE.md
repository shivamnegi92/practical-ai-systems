## What changed?

## Evidence and evaluation
- [ ] Synthetic or clearly licensed data; no sensitive or employer-confidential material.
- [ ] Evaluation cases and `eval/results.json` updated where behavior changes.
- [ ] Known limitations and failure modes documented.
- [ ] Result claims match the measured scope and sample count.

## Validation
- [ ] `python3 scripts/evaluate_systems.py --check --write`
- [ ] `python3 -m unittest discover -s common -t . -v`
- [ ] `python3 -m unittest discover -s systems -p 'test_*.py' -v`
- [ ] `python3 scripts/render_systems.py --write && python3 scripts/render_systems.py`
- [ ] `python3 -m unittest discover -s tests -v`
- [ ] `git diff --check`
