import itertools
import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


def brute_min_cut(edges, n):
    best = len(edges)
    for mask in range(1, 2 ** n - 1):
        best = min(best, sum(1 for u, v in edges if (mask >> u & 1) != (mask >> v & 1)))
    return best


class TestRandomized(unittest.TestCase):
    def test_las_vegas(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            vals = [rng.randint(0, 50) for _ in range(rng.randint(1, 40))]
            k = rng.randrange(len(vals))
            self.assertEqual(ex.quickselect(vals, k, rng)[0], sorted(vals)[k])
            self.assertEqual(sol.randomized_quicksort(vals, rng), sorted(vals))
        _, comps = ex.quickselect(list(range(20000, 0, -1)), 10000, rng)
        self.assertLess(comps, 20000 * 8)

    def test_monte_carlo(self) -> None:
        rng = random.Random(2)
        wrong = 0
        for _ in range(100):
            n = rng.randint(1, 5)
            a = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
            b = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)]
            c = [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
            self.assertTrue(ex.freivalds(a, b, c, 10, rng))          # never wrong when equal
            c[rng.randrange(n)][rng.randrange(n)] += 1
            wrong += ex.freivalds(a, b, c, 10, rng)
        self.assertLessEqual(wrong, 1)
        for _ in range(30):
            n = rng.randint(2, 7)
            edges = [(u, v) for u, v in itertools.combinations(range(n), 2) if rng.random() < 0.6]
            if not edges:
                continue
            self.assertGreaterEqual(ex.karger_cut(edges, n, rng), brute_min_cut(edges, n))
            self.assertEqual(ex.min_cut_repeated(edges, n, 200, rng), brute_min_cut(edges, n))
        self.assertTrue(sol.polynomial_identity(lambda x: (x + 1) ** 2, lambda x: x * x + 2 * x + 1, 2, 10, rng))
        self.assertFalse(sol.polynomial_identity(lambda x: (x + 1) ** 2, lambda x: x * x + 1, 2, 10, rng))

    def test_examples(self) -> None:
        rng = random.Random(3)
        self.assertLess(ex.load_balance(100000, 1000, rng, 2), ex.load_balance(100000, 1000, rng, 1))
        i, _ = sol.las_vegas_find([7, 0] * 50, 7, rng)
        self.assertEqual(i % 2, 0)


if __name__ == "__main__":
    unittest.main()
