import math
import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestSums(unittest.TestCase):
    def test_arithmetic(self) -> None:
        for n in range(1, 200):
            self.assertEqual(ex.arithmetic_sum(1, n, n), ex.sum_loop(1, n))
        self.assertEqual(ex.arithmetic_sum(15, 60, 10), ex.sum_loop(15, 60, 5))
        for n in range(0, 100):
            self.assertEqual(ex.sum_of_squares(n), sum(k * k for k in range(1, n + 1)))

    def test_geometric(self) -> None:
        for ratio in (2, 3, 0.5, 1):
            for terms in range(0, 15):
                self.assertAlmostEqual(ex.geometric_sum(1, ratio, terms), ex.geometric_sum_loop(1, ratio, terms))
        self.assertEqual(ex.geometric_sum(1, 2, 10), 1023)
        self.assertLess(ex.geometric_sum(1, 0.5, 20), 2)          # approaches 2 but never reaches it
        self.assertAlmostEqual(ex.geometric_sum(1, 0.5, 20), 2, places=5)
        self.assertEqual(ex.chessboard_grains(), 18_446_744_073_709_551_615)
        self.assertEqual(ex.total_backoff_wait(6), 63)
        self.assertEqual(ex.nodes_in_full_tree(10), 1023)


class TestLogs(unittest.TestCase):
    def test_floor_ceil(self) -> None:
        for n in range(1, 5000):
            self.assertTrue(2 ** ex.floor_log2(n) <= n < 2 ** (ex.floor_log2(n) + 1))
            self.assertTrue(2 ** ex.ceil_log2(n) >= n)
            self.assertTrue(ex.ceil_log2(n) == 0 or 2 ** (ex.ceil_log2(n) - 1) < n)
            self.assertEqual(ex.halvings_until_one(n), ex.floor_log2(n))
        with self.assertRaises(ValueError):
            ex.floor_log2(0)

    def test_applications(self) -> None:
        self.assertEqual(ex.tournament_rounds(64), 6)
        self.assertEqual(ex.tournament_rounds(100), 7)
        self.assertEqual(ex.decimal_digits(2 ** 100), 31)
        self.assertEqual(ex.decimal_digits(9), 1)
        self.assertAlmostEqual(ex.log_base(1000, 10), 3)
        self.assertAlmostEqual(ex.years_to_double(7), 10.24, places=2)
        self.assertLess(abs(ex.harmonic(1000) - math.log(1000)), 1)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.seats_in_theater(20, 2, 15), sum(20 + 2 * k for k in range(15)))
        for n in range(0, 30):
            self.assertEqual(sol.nested_loop_steps(n), sum(i for i in range(n)))
        self.assertAlmostEqual(sol.savings_plan(100, 12, 1.05), 1591.71, places=2)
        self.assertEqual(sol.phone_book_halvings(1_000_000), 20)
        for difference in sol.simplify_log_expression().values():
            self.assertAlmostEqual(difference, 0)
        self.assertEqual(sol.levels_for_items(1_000_000, 100), 3)
        self.assertEqual(sol.levels_for_items(1, 2), 0)


if __name__ == "__main__":
    unittest.main()
