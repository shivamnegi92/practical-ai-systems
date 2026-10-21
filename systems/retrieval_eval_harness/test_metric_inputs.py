import unittest
from systems.retrieval_eval_harness.app import recall_at_k, ndcg_at_k, evaluate_ranking, compare_strategies


class MetricInputTests(unittest.TestCase):
    def test_invalid_cutoffs_are_rejected_at_every_boundary(self):
        for k in (-1, 1.5, float('nan'), float('inf'), True, '2', None):
            calls = [lambda: recall_at_k([], set(), k), lambda: ndcg_at_k([], {}, k),
                     lambda: evaluate_ranking([], {}, k), lambda: compare_strategies({}, [], k)]
            for call in calls:
                with self.subTest(k=k), self.assertRaises(ValueError): call()

    def test_invalid_grades_are_rejected_before_scoring(self):
        for grade in (-1, float('nan'), float('inf'), True, '1', None):
            for call in (lambda: ndcg_at_k([], {'a': grade}, 1), lambda: evaluate_ranking([], {'a': grade}, 1)):
                with self.subTest(grade=grade), self.assertRaises(ValueError): call()

    def test_zero_integral_cutoffs_and_fractional_grades(self):
        self.assertEqual(recall_at_k(['a'], {'a'}, 0), 0)
        self.assertEqual(ndcg_at_k(['a'], {'a': .5}, 0), 0)
        self.assertEqual(ndcg_at_k(['a'], {'a': .5}, 1.0), 1)
        self.assertEqual(recall_at_k(['a'], {'a'}, 1.0), 1)
