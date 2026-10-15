# Repository hygiene checks

Scan local files for a tiny set of obvious patterns; this is not a security scanner.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.repo_guard.evaluate
```

## Evaluate and test

```bash
python3 -m systems.repo_guard.evaluate
python3 -m unittest systems.repo_guard.test_guard
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

The eight-file Python/web matrix is measured through the public scanner, not a separate whole-text regex approximation. Each Python fixture is written in an isolated temporary repository, preserving its extension and line boundaries. File-level precision is 1.0 and recall is 4/6: split-line chmod and wget-to-shell remain two known misses. The text-file shell snippet correctly produces no finding. The two-finding file counts as one positive file; finding counts are not the metric. See [val/results.json](eval/results.json).

## Known limitations

- The scanner remains line-scoped and recognizes only a few shell patterns. This evaluator fix does not expand detection. All examples are synthetic; passing this matrix is not security certification.

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
