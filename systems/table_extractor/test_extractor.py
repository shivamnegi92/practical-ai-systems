import unittest

from systems.table_extractor.app import extract_table


class TableExtractorTests(unittest.TestCase):
    def test_builds_a_clean_grid(self):
        lines = [
            {"text": "Name", "bbox": [0, 0, 30, 10]},
            {"text": "Qty", "bbox": [100, 0, 130, 10]},
            {"text": "Price", "bbox": [200, 0, 240, 10]},
            {"text": "Widget", "bbox": [0, 20, 40, 30]},
            {"text": "5", "bbox": [100, 20, 110, 30]},
            {"text": "$10", "bbox": [200, 20, 220, 30]},
        ]
        grid = extract_table(lines)
        self.assertEqual(grid, [["Name", "Qty", "Price"], ["Widget", "5", "$10"]])

    def test_tolerates_small_y_jitter_within_a_row(self):
        lines = [
            {"text": "A", "bbox": [0, 0, 10, 8]},
            {"text": "B", "bbox": [60, 2, 70, 10]},
            {"text": "C", "bbox": [120, 1, 130, 9]},
        ]
        grid = extract_table(lines)
        self.assertEqual(grid, [["A", "B", "C"]])

    def test_empty_input_returns_empty_grid(self):
        self.assertEqual(extract_table([]), [])

    def test_invalid_gap_raises_value_error(self):
        lines = [{"text": "A", "bbox": [0, 0, 10, 8]}]
        for invalid in [-1, -0.01, "5", True, float("nan"), float("inf")]:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    extract_table(lines, row_gap=invalid)
                with self.assertRaises(ValueError):
                    extract_table(lines, col_gap=invalid)


if __name__ == "__main__":
    unittest.main()
