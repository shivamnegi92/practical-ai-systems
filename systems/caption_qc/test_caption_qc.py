import unittest

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

    def test_rejects_non_string_caption(self):
        with self.assertRaises(TypeError):
            check_caption(None)
        with self.assertRaises(TypeError):
            check_caption(123)

    def test_rejects_invalid_bounds(self):
        with self.assertRaises(ValueError):
            check_caption("A valid caption", min_words=-1)
        with self.assertRaises(ValueError):
            check_caption("A valid caption", min_words=10, max_words=5)


if __name__ == "__main__":
    unittest.main()
