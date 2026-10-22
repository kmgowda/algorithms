import math
import random
import unittest

import ch07_solutions as sol


def brute(f, budget):
    n = 1
    while f(n + 1) <= budget:
        n += 1
    return n


class TestChapter7Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.largest_fitting(lambda n: n, 1), (1, 1))
        self.assertEqual(sol.largest_fitting(lambda n: n, 2), (2, 3))
        self.assertEqual(sol.largest_fitting(lambda n: n, 3), (3, 3))
        self.assertEqual(sol.largest_fitting(lambda n: 2 ** n, 2), (1, 1))

    def test_one_second(self) -> None:
        rates = [lambda n: n, lambda n: n * math.log2(n), lambda n: n * n, lambda n: n ** 3, lambda n: 2 ** n]
        self.assertEqual([sol.largest_fitting(f, 1e7)[0] for f in rates], [10_000_000, 526_172, 3_162, 215, 23])
        self.assertEqual(sol.largest_fitting(rates[1], 1e7), (526_172, 39))

    def test_against_brute_force(self) -> None:
        rng = random.Random(7)
        for _ in range(300):
            a, b = rng.randint(1, 5), rng.randint(1, 3)
            budget = rng.randint(a, 5000)
            f = (lambda a, b: lambda n: a * n ** b)(a, b)
            n, evals = sol.largest_fitting(f, budget)
            self.assertEqual(n, brute(f, budget))
            self.assertEqual(evals, 2 * int(math.log2(n)) + 1)


if __name__ == "__main__":
    unittest.main()
