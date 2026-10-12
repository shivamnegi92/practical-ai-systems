# Entity spans and error analysis

Find simple person, location, date, and money spans and report exact-span metrics.

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

Eight handcrafted synthetic sentences include three location examples and a correctly labelled Buenos Aires case that still fails. The examples deliberately expose the narrow rule-based model's error modes (dates/capitalized entities are ambiguous). These scores are a fixture regression signal, not a language-wide NER estimate. See [`eval/results.json`](eval/results.json) for the measured macro averages. The web port adds the same four location cases to its own existing fixture set.

## Known limitations

- A four-place gazetteer (New York, San Francisco, Los Angeles, New Delhi) retypes matching two-word capitalized spans as LOCATION. Buenos Aires is outside it and remains misclassified as PERSON in the evaluation. Unknown places, longer names, and person/place homonyms remain ambiguous; this is not general named-entity recognition.

- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
- The implementation is intentionally small and deterministic. It does not establish production-readiness, security, or fitness for any specific deployment.
- Read the source, evaluation case file, and printed method/scope before reusing.
