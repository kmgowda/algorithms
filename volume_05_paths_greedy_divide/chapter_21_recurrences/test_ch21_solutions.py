import math
import unittest

import ch21_examples as ex
import ch21_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_exact_n_log_n(self) -> None:
        for k in range(1, 15):
            n = 2 ** k
            self.assertEqual(ex.solve(n, [2, 2], lambda m: m, 0.0), n * k)

    def test_predicted_ratio(self) -> None:
        for a, b, d in ((4, 2, 1), (3, 2, 1), (2, 2, 2), (8, 2, 2)):
            self.assertAlmostEqual(sol.doubling_ratio(2 ** 16, a, b, lambda n, d=d: n ** d), sol.predicted_ratio(a, b, d), delta=0.01)
        self.assertAlmostEqual(sol.doubling_ratio(2 ** 16, 2, 2, lambda n: n), 2 * 17 / 16, places=9)

    def test_n_log_n_split(self) -> None:
        for k in (8, 12, 16, 20):
            r = sol.doubling_ratio(2 ** k, 2, 2, lambda n: n * math.log2(n))
            self.assertAlmostEqual(r, 2 * (k + 2) / k, places=9)          # T(2^k) = 2^k k(k + 1) / 2 exactly
            self.assertGreater(r, 2 * (k + 1) / k)       # more than an n log n ratio


if __name__ == "__main__":
    unittest.main()
