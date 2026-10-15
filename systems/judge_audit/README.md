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

The shared 14-row Python/web matrix preserves both original fixture sets, including their two deliberate rater disagreements. It adds numeric and negation contradictions plus an exact-match control. `human_a`/`human_b` are synthetic labels, not newly collected human ratings. See [`eval/results.json`](eval/results.json) for measured agreement and kappa; these are agreement mechanics, not an LLM-judge assessment.

## Known limitations

- Lexical overlap can endorse $80 against $8, can/cannot reversals and explicit SMS negation. Both ports keep these three contradictions as misses against the agreed unsupported labels; no threshold, judge algorithm or rater labels were tuned to hide them. Exact text overlap remains a positive control.

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
