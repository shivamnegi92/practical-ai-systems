import unittest
import json
from pathlib import Path

from systems.caption_qc.app import check_caption


class CaptionQcTests(unittest.TestCase):
    def test_good_caption_passes(self):
        result = check_caption(
            "A golden retriever running across a sunny beach.", ["retriever", "beach"]
        )
        self.assertTrue(result["passed"])

    def test_banned_phrase_fails(self):
        result = check_caption("image of a cat.")
        self.assertFalse(result["passed"])
        self.assertTrue(any("banned_phrase" in r for r in result["reasons"]))

    def test_too_short_fails(self):
        result = check_caption("Red car.", ["car"])
        self.assertIn("too_short", result["reasons"])

    def test_missing_keyword_fails(self):
        result = check_caption("A sunny beach with waves.", ["dog"])
        self.assertTrue(any("missing_keywords" in r for r in result["reasons"]))


if __name__ == "__main__":
    unittest.main()


class CaptionEvaluationTests(unittest.TestCase):
    def test_gold_labels_expose_four_current_misses(self):
        cases = json.loads((Path(__file__).parent / "eval/cases.json").read_text())
        missed = [c["caption"] for c in cases if check_caption(c["caption"], c["required_keywords"])["passed"] != c["gold_pass"]]
        self.assertEqual(missed, ["image   of a dog", "picture\tof a dog", "A carpet covers the floor.", "A cart rests near the wall."])
        from systems.caption_qc.evaluate import evaluate
        self.assertEqual(evaluate()["cases"], 16)
        self.assertEqual(evaluate()["qc_accuracy"], 0.75)
