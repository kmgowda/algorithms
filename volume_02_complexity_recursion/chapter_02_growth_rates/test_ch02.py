import math
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestGrowth(unittest.TestCase):
    def test_row(self) -> None:
        row = ex.growth_row(16)
        self.assertEqual(row["log n"], 4)
        self.assertEqual(row["n log n"], 64)
        self.assertEqual(row["2^n"], 65536)
        self.assertEqual(row["n!"], math.factorial(16))

    def test_bars(self) -> None:
        lines = ex.ascii_bars({"a": 10, "b": 5}, width=10)
        self.assertEqual(lines[0].count("#"), 10)
        self.assertEqual(lines[1].count("#"), 5)

    def test_crossovers(self) -> None:
        self.assertEqual(ex.crossover(lambda n: 100 * n, lambda n: n * n), 101)
        self.assertEqual(ex.crossover(lambda n: n ** 3, lambda n: 2 ** n), 10)
        self.assertIsNone(ex.crossover(lambda n: n * n, lambda n: n, limit=1000))

    def test_largest_n(self) -> None:
        self.assertEqual(ex.largest_n_within(1e9, lambda n: n), 1_000_000_000)
        self.assertEqual(ex.largest_n_within(1e9, lambda n: n * n), 31622)
        self.assertEqual(ex.largest_n_within(1e9, lambda n: 2 ** n), 29)
        self.assertEqual(ex.largest_n_within(1e9, math.factorial), 12)
        self.assertEqual(ex.largest_n_within(0.5, lambda n: n), 0)
        for budget in (1, 7, 100, 12345):
            n = ex.largest_n_within(budget, lambda k: k * k)
            self.assertTrue(n * n <= budget < (n + 1) * (n + 1))

    def test_users_and_money(self) -> None:
        self.assertEqual(ex.users_supported(4, 1e6, lambda n: n * n), 2000)
        self.assertEqual(ex.simple_vs_compound(1000, 7, 30), (3100.0, 7612.26))


class TestSolutions(unittest.TestCase):
    def test_rank(self) -> None:
        self.assertEqual(sol.rank_by_growth(["n^2", "log n", "2^n", "n", "1", "n log n"]),
                         ["1", "log n", "n", "n log n", "n^2", "2^n"])

    def test_crossover_and_bacteria(self) -> None:
        n = sol.crossover_constant_vs_quadratic()
        self.assertTrue(2 * n * n > 50 * n + 1000)
        self.assertFalse(2 * (n - 1) ** 2 > 50 * (n - 1) + 1000)
        self.assertEqual(sol.bacteria_hours(1, 1_000_000), 20)
        self.assertEqual(sol.bacteria_hours(5, 5), 0)

    def test_budget_and_gain(self) -> None:
        self.assertEqual(sol.fits_in_budget(1e6), {"n": 1_000_000, "n^2": 1000, "2^n": 19})
        gain = sol.faster_computer_gain(100)
        self.assertAlmostEqual(gain["n^2"], 10)
        self.assertAlmostEqual(gain["2^n"], math.log2(100))


if __name__ == "__main__":
    unittest.main()
