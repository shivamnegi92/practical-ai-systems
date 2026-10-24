# Voice-agent transcript evaluation

Score task completion, forbidden actions, and latency from synthetic transcripts.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.voice_eval.evaluate
```

## Evaluate and test

```bash
python3 -m systems.voice_eval.evaluate
python3 -m unittest systems.voice_eval.test_voice
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

The shared eight-call Python/web matrix retains all three original Python calls and the browser demo. Explicit gold task/safety labels expose two negated false successes: task-success accuracy is 6/8 (0.75), while the heuristic reports success on 7/8. Two planted forbidden actions are detected (safety accuracy 8/8). Rates describe predictions; accuracy compares them with synthetic gold. Latency is fixture metadata, not measured execution; Python keeps the upper-middle aggregation convention. Existing web demo fields and `matches_expected` remain demo-only, alongside the new aggregate metrics. See [`eval/results.json`](eval/results.json).

## Known limitations

- Loose term matching accepts “appointment was not moved” and “refund was not issued” as completed requirements. The new gold labels stay false; scorer runtime is unchanged. Missing-requirement and case-insensitive forbidden-action controls pass. No audio, speech recognition, live call, real action or production safety study was run.

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
