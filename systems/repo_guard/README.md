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

The toy regex rules match all **4/4** synthetic fixtures (precision/recall 1.00). Fixtures contain only obvious private-key markers, an example access-key-shaped string, a risky pipe-to-shell line, and clean text. Real secret scanning needs maintained scanners and review; this is neither comprehensive nor a security certification. See [`eval/results.json`](eval/results.json).

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
