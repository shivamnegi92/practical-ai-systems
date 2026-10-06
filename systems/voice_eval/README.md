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

On three synthetic calls, the rubric marks task completion **1.00** and detects a forbidden-action rate of **0.33**. Median latency **980 ms** is copied from fixture metadata, not measured execution. One planted refund-action violation is found. This verifies scoring logic only; it is not evidence of actual voice-agent quality or safe deployment. See [`eval/results.json`](eval/results.json).

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
