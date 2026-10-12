import unittest

from systems.faq_router.app import route


class FaqRouterTests(unittest.TestCase):
    def test_billing_inflections(self):
        for text in ("my card was charged twice", "the card charges twice", "charging twice", "payments"):
            with self.subTest(text=text):
                self.assertEqual(route(text), "billing_question")

    def test_contiguous_log_in_phrase_retains_stopword(self):
        self.assertEqual(route("I can't log in"), "technical_issue")
        self.assertEqual(route("log in"), "technical_issue")
        for text in ("log", "in log", "log outside in"):
            with self.subTest(text=text):
                self.assertEqual(route(text), "unknown")

    def test_normalized_keywords_preserve_tie_order(self):
        self.assertEqual(route("hello payment"), "greeting")
        self.assertEqual(route("greetings"), "greeting")

    def test_greeting(self):
        self.assertEqual(route("Hi there, how are you?"), "greeting")

    def test_cancel_request(self):
        self.assertEqual(route("I want to cancel my subscription"), "cancel_request")

    def test_technical_issue(self):
        self.assertEqual(route("The app keeps crashing and showing an error"), "technical_issue")

    def test_unknown_falls_back(self):
        self.assertEqual(route("asdkj qwleoi zzxcv"), "unknown")


if __name__ == "__main__":
    unittest.main()
