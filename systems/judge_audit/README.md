# Judge agreement audit

Compare a transparent lexical support heuristic with two synthetic human ratings.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.judge_audit.evaluate
```

## Evaluate and test

```bash
python3 -m systems.judge_audit.evaluate
python3 -m unittest systems.judge_audit.test_judge
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

On 6 synthetic claims, the lexical heuristic agrees with rater A **0.50** of the time; human inter-rater kappa is **0.67**, while heuristic-vs-rater-A kappa is **0.00**. This small example demonstrates why judge agreement must be measured against people; it does not evaluate an LLM judge. See [`eval/results.json`](eval/results.json).

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
