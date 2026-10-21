import unittest
from systems.entity_extraction.app import score


class ExactSpanPositions(unittest.TestCase):
    def test_wrong_occurrence_is_not_a_match(self):
        gold = [{"text": "Jane Doe", "type": "PERSON", "start": 0, "end": 8}]
        wrong = [{**gold[0], "start": 20, "end": 28}]
        self.assertEqual(score(wrong, gold), {"precision": 0, "recall": 0, "f1": 0})

    def test_repeated_text_at_different_positions_is_not_collapsed(self):
        first = {"text": "Jane Doe", "type": "PERSON", "start": 0, "end": 8}
        second = {**first, "start": 20, "end": 28}
        result = score([first], [first, second])
        self.assertEqual(result["precision"], 1)
        self.assertEqual(result["recall"], 0.5)

    def test_identical_duplicate_annotations_do_not_inflate_metrics(self):
        entity = {"text": "Jane Doe", "type": "PERSON", "start": 0, "end": 8}
        self.assertEqual(score([entity, entity], [entity])["f1"], 1)
