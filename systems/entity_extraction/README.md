# Entity spans and error analysis

Find simple person, date, and money spans and report exact-span metrics.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.entity_extraction.evaluate
```

## Evaluate and test

```bash
python3 -m systems.entity_extraction.evaluate
python3 -m unittest systems.entity_extraction.test_entity
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

Four handcrafted synthetic sentences produce macro-averaged exact-span precision **0.63**, recall **0.67**, F1 **0.63**. The examples deliberately expose the narrow rule-based model's error modes (dates/capitalized entities are ambiguous). These scores are a fixture regression signal, not a language-wide NER estimate. See [`eval/results.json`](eval/results.json).

## Known limitations

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
