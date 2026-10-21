import unittest
from systems.table_extractor.app import extract_table


class FragmentTests(unittest.TestCase):
    def test_fragments_keep_left_to_right_text_and_row_boundaries(self):
        lines = [
            {"text": "York", "bbox": [20, 0, 30, 8]},
            {"text": "2", "bbox": [100, 0, 110, 8]},
            {"text": "New", "bbox": [0, 0, 10, 8]},
            {"text": "Los", "bbox": [0, 20, 10, 28]},
            {"text": "Angeles", "bbox": [20, 20, 30, 28]},
        ]
        self.assertEqual(extract_table(lines), [["New York", "2"], ["Los Angeles", ""]])

    def test_repeated_fragments_are_preserved(self):
        self.assertEqual(extract_table([
            {"text": "ha", "bbox": [0, 0, 10, 8]},
            {"text": "ha", "bbox": [20, 0, 30, 8]},
        ]), [["ha ha"]])
