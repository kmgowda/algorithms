import math
import unittest

import ch33_examples as ex
import ch33_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_evaluations_logarithmic(self) -> None:
        for rate in ("n", "n log n", "n^2", "n^3", "2^n", "n!"):
            for budget in (1, 10, 10 ** 4, 10 ** 8):
                n, evals = sol.largest_input_counted(rate, budget)
                self.assertEqual(n, ex.largest_input(rate, budget))
                self.assertLessEqual(evals, 2 * math.log2(n + 2) + 3)
        self.assertEqual(sol.largest_input_counted("n^2", 10 ** 8), (10000, 28))

    def test_plan_sites(self) -> None:
        s, h = ex.town(12, 200, 30)
        how, chosen, r = sol.plan_sites(s, h, 3, 10 ** 6)
        self.assertEqual((how, chosen), ("exact", [3, 4, 6]))
        how2, chosen2, r2 = sol.plan_sites(s, h, 3, 1000)
        self.assertEqual(how2, "greedy + swaps")
        self.assertGreaterEqual(r2, r - 1e-12)

    def test_crossover(self) -> None:
        f, g = (lambda n: 50 * n * math.log2(n)), (lambda n: n * n)
        n = sol.crossover(f, g)
        self.assertEqual(n, 439)
        self.assertGreater(f(10), g(10))
        self.assertTrue(all(f(m) < g(m) for m in range(439, 5000)))


if __name__ == "__main__":
    unittest.main()
