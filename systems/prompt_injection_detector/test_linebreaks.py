import unittest
from systems.prompt_injection_detector.app import scan


class LineBreakTests(unittest.TestCase):
    def test_bounded_patterns_match_across_line_endings(self):
        for newline in ("\n", "\r\n"):
            for prefix, suffix, expected in [("ignore", "instructions", "override_instructions"), ("show", "system prompt", "reveal_prompt"), ("act as", "unrestricted", "role_override"), ("disregard", "safety", "disregard_safety")]:
                text = prefix + newline + suffix
                with self.subTest(text=text):
                    self.assertIn({"pattern": expected, "match": text}, scan(text)["matches"])

    def test_character_limits_and_clean_controls_remain(self):
        self.assertFalse(scan("ignore" + "\n" * 31 + "instructions")["flagged"])
        self.assertFalse(scan("show" + "\n" * 21 + "system prompt")["flagged"])
        self.assertFalse(scan("Please summarize this document.")["flagged"])
