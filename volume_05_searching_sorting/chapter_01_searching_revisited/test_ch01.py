import math
import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestSearch(unittest.TestCase):
    def test_linear_and_binary(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            items = sorted(rng.sample(range(100), rng.randint(0, 20)))
            t = rng.randint(-5, 105)
            expected = items.index(t) if t in items else -1
            self.assertEqual(ex.binary_search(items, t), expected)
            self.assertEqual(sol.binary_search_recursive(items, t), expected)
            self.assertEqual(ex.linear_search(items, t), expected)

    def test_first_true(self) -> None:
        for n in range(0, 20):
            for cut in range(0, n + 2):
                self.assertEqual(ex.first_true(0, n, lambda x: x >= cut), min(cut, n + 1))

    def test_answers(self) -> None:
        for n in range(0, 2000):
            self.assertEqual(ex.integer_sqrt(n), math.isqrt(n))
        with self.assertRaises(ValueError):
            ex.integer_sqrt(-1)
        self.assertEqual(ex.monkey_eating_speed([3, 6, 7, 11], 8), 4)
        self.assertEqual(ex.monkey_eating_speed([30, 11, 23, 4, 20], 5), 30)
        self.assertEqual(ex.split_shelves([7, 2, 5, 10, 8], 2), 18)
        self.assertEqual(ex.first_bad_version(100, lambda v: v >= 64), 64)
        self.assertEqual(ex.first_bad_version(1, lambda v: True), 1)

    def test_split_shelves_brute(self) -> None:
        import itertools
        rng = random.Random(2)
        for _ in range(100):
            w = [rng.randint(1, 9) for _ in range(rng.randint(1, 7))]
            k = rng.randint(1, len(w))
            best = math.inf
            for cuts in itertools.combinations(range(1, len(w)), k - 1):
                bounds = (0,) + cuts + (len(w),)
                best = min(best, max(sum(w[a:b]) for a, b in zip(bounds, bounds[1:])))
            self.assertEqual(ex.split_shelves(w, k), best)


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.min_ship_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15)
        self.assertEqual(sol.earliest_bloom_day([1, 10, 3, 10, 2], 3, 1), 3)
        self.assertEqual(sol.earliest_bloom_day([1, 10, 3, 10, 2], 3, 2), -1)
        self.assertEqual(sol.earliest_bloom_day([7, 7, 7, 7, 12, 7, 7], 2, 3), 12)
        for n in range(0, 500):
            r = sol.cube_root_floor(n)
            self.assertTrue(r ** 3 <= n < (r + 1) ** 3)


if __name__ == "__main__":
    unittest.main()
