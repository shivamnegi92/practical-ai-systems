import json
import tempfile
import unittest
from pathlib import Path

from common.evaluation import cohen_kappa, mean, percentile, prf, write_results
from common.llm import StubLLM, from_env, parse_json
from common.text import BM25, sentences, tokenize


class TextTests(unittest.TestCase):
    def test_tokenize_lowercases_stems_and_drops_stopwords(self):
        self.assertEqual(tokenize("The Refund POLICY for orders"), ["refund", "policy", "order"])

    def test_bm25_ranks_matching_document_first(self):
        index = BM25({"a": "refund policy for damaged items", "b": "office wifi password reset"})
        hits = index.search("how do refunds for damaged items work", k=2)
        self.assertEqual(hits[0][0], "a")
        self.assertTrue(all(score > 0 for _, score in hits))

    def test_bm25_omits_zero_score_documents(self):
        index = BM25({"a": "alpha beta", "b": "gamma delta"})
        self.assertEqual([doc for doc, _ in index.search("alpha", k=5)], ["a"])

    def test_sentences_split_on_terminal_punctuation(self):
        self.assertEqual(sentences("One. Two? Three!"), ["One.", "Two?", "Three!"])


class EvaluationTests(unittest.TestCase):
    def test_prf_handles_zero_division(self):
        self.assertEqual(prf(0, 0, 0), {"precision": 0.0, "recall": 0.0, "f1": 0.0})
        self.assertEqual(prf(2, 2, 0)["precision"], 0.5)

    def test_percentile_and_mean(self):
        self.assertEqual(percentile([1, 2, 3, 4], 50), 2.5)
        self.assertEqual(mean([]), 0.0)

    def test_cohen_kappa_perfect_and_chance(self):
        self.assertEqual(cohen_kappa(["A", "B", "A"], ["A", "B", "A"]), 1.0)
        self.assertEqual(cohen_kappa(["A", "A"], ["A", "A"]), 1.0)
        self.assertLess(cohen_kappa(["A", "B", "A", "B"], ["B", "A", "B", "A"]), 0)

    def test_write_results_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "results.json"
            write_results(path, "demo", "baseline", {"b": 0.123456, "a": 1}, cases=3)
            data = json.loads(path.read_text())
            self.assertEqual(data["metrics"], {"a": 1, "b": 0.1235})
            self.assertEqual(data["dataset"]["cases"], 3)


class LLMTests(unittest.TestCase):
    def test_stub_records_calls(self):
        llm = StubLLM(lambda prompt: prompt.upper())
        self.assertEqual(llm.complete("hi"), "HI")
        self.assertEqual(llm.calls, ["hi"])

    def test_parse_json_extracts_embedded_object(self):
        self.assertEqual(parse_json('Sure! {"a": 1} hope that helps'), {"a": 1})
        self.assertIsNone(parse_json("no json here"))

    def test_from_env_rejects_unknown_provider(self):
        with self.assertRaises(ValueError):
            from_env("nope")


if __name__ == "__main__":
    unittest.main()
