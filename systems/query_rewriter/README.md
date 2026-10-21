# Synonym query rewriter

Expand a query with a small hand-built synonym list before BM25 retrieval, and measure the recall it recovers.

**Level:** starter · **Runs locally:** yes · **Credentials:** none · **Dependencies:** Python standard library only

## Quickstart

Run from the repository root:

```bash
python3 -m systems.query_rewriter.app "What is the price?"
```

## Evaluate and test

```bash
python3 -m systems.query_rewriter.evaluate
python3 -m unittest systems.query_rewriter.test_rewriter
```

The evaluation uses the small synthetic dataset shipped in this folder. Results describe this implementation on those fixtures only; they are not general performance claims.

## Results snapshot

See [`eval/results.json`](eval/results.json). On a 4-document synthetic corpus, baseline recall@1 is low because 3 of 4 queries use a word absent from the target document; expansion recovers all 4 by injecting the matching synonym.

## Known limitations

- The synonym list is hand-picked for this fixture and is not a general thesaurus; it will not expand any term outside the six entries defined in `app.py`.
- Expansion can also hurt precision by pulling in documents that match only on the injected synonym; this baseline does not re-rank or validate expanded hits.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.

Declared synonym keys use the same tokenization/stemming as queries, so aliases such as `pricing` remain reachable after stemming. The original query is retained; this does not add new synonym terms or general semantic understanding.
