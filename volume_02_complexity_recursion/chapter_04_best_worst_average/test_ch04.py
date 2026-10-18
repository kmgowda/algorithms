import unittest

import ch04_examples as ex
import ch04_solutions as sol


class TestCases(unittest.TestCase):
    shelf = ["Atlas", "Birds", "Cats", "Dune", "Emma"]

    def test_search_cases(self) -> None:
        self.assertEqual(ex.comparisons_to_find(self.shelf, "Atlas"), 1)
        self.assertEqual(ex.comparisons_to_find(self.shelf, "Emma"), 5)
        self.assertEqual(ex.comparisons_to_find(self.shelf, "Zebra"), 5)

    def test_averages(self) -> None:
        for n in (1, 5, 100):
            self.assertAlmostEqual(ex.average_comparisons_exact(n), (n + 1) / 2)
        self.assertAlmostEqual(ex.simulated_average(100, 20_000), 50.5, delta=1.0)
        self.assertAlmostEqual(ex.expected_comparisons([0.2] * 5), 3.0)
        self.assertAlmostEqual(ex.expected_comparisons([0.5, 0.2, 0.15, 0.1, 0.05]), 2.0)
        with self.assertRaises(ValueError):
            ex.expected_comparisons([0.5, 0.2])

    def test_insert_card(self) -> None:
        self.assertEqual(ex.insert_card([2, 5, 7], 9), ([2, 5, 7, 9], 0))
        self.assertEqual(ex.insert_card([2, 5, 7], 1), ([1, 2, 5, 7], 3))
        self.assertEqual(ex.insert_card([], 4), ([4], 0))
        self.assertEqual(ex.insert_card([2, 5, 7], 5), ([2, 5, 5, 7], 1))

    def test_duplicates(self) -> None:
        self.assertEqual(ex.first_duplicate_comparisons([3, 3, 1, 2]), 1)
        self.assertEqual(ex.first_duplicate_comparisons([1, 2, 3, 4]), 6)

    def test_industry(self) -> None:
        self.assertAlmostEqual(ex.expected_latency(0.9, 2, 80), 9.8)
        with self.assertRaises(ValueError):
            ex.expected_latency(1.5, 2, 80)
        requests = ["Emma"] * 8 + ["Dune"] * 4 + ["Atlas"]
        fixed, moving = ex.total_cost_move_to_front(self.shelf, requests)
        self.assertEqual(fixed, 8 * 5 + 4 * 4 + 1)
        self.assertLess(moving, fixed)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.cases_for_find_max(10), (9, 9))
        for size in range(1, 7):
            self.assertAlmostEqual(sol.average_shifts_over_all_orders(size), size * (size - 1) / 4)
        self.assertAlmostEqual(sol.expected_with_missing(10, 0.5), 0.5 * 5.5 + 0.5 * 10)
        self.assertAlmostEqual(sol.break_even_hit_rate(2, 80, 10), 70 / 78)
        self.assertEqual(sol.break_even_hit_rate(2, 80, 100), 0.0)
        with self.assertRaises(ValueError):
            sol.break_even_hit_rate(2, 80, 1)
        self.assertEqual(sol.worst_input_for_search(["a", "zzz"]), "zzzz")


if __name__ == "__main__":
    unittest.main()
