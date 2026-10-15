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

See [`eval/results.json`](eval/results.json). The shared ten-query matrix preserves both original Python/web query sets and adds morphology failures plus a `remove` control. The original four-document corpora remain unchanged: Python d2 is weather and d4 is generic deletion, while web d2 is shipping and d4 describes account deletion. Metrics must therefore be read separately; corpus differences and tokenization can affect top-one rankings.

## Known limitations

- Stemming changes `pricing` to `pric` and `erasing` to `eras` before the dictionary lookup, so neither gains the intended synonym. The new gold targets retain price/deletion intent; `remove` still expands to `delete` as a control. Runtime, synonym dictionary and corpus are unchanged; this PR measures the misses instead of tuning to the cases.
- The synonym list is hand-picked for this fixture and is not a general thesaurus; it will not expand any term outside the six entries defined in `app.py`.
- Expansion can also hurt precision by pulling in documents that match only on the injected synonym; this baseline does not re-rank or validate expanded hits.
- Synthetic data is not representative of real production traffic. Expand and independently label cases before relying on these results.
