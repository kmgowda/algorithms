import math
import random
import unittest
from collections import Counter

import ch19_examples as ex
import ch19_solutions as sol


class TestChapter19Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.distinct_counts([]), [])
        self.assertEqual(sol.distinct_counts([47]), [(47, 1)])
        self.assertEqual(sol.distinct_counts([47, 47]), [(47, 2)])
        self.assertEqual(sol.distinct_counts([12, 47]), [(12, 1), (47, 1)])

    def test_catalogue(self) -> None:
        self.assertEqual(sol.distinct_counts(ex.CATALOGUE),
                         [(12, 1), (25, 2), (31, 1), (47, 3), (58, 1), (63, 1), (70, 1), (84, 1), (91, 1)])

    def test_against_brute_force(self) -> None:
        rng = random.Random(19)
        for _ in range(1000):
            a = sorted(rng.randint(1, 15) for _ in range(rng.randint(0, 30)))
            self.assertEqual(sol.distinct_counts(a), sorted(Counter(a).items()))

    def test_looks_per_search(self) -> None:
        """Thinking Problem 1: a lower bound on n values makes between floor(log2(n + 1)) and floor(log2 n) + 1 looks."""
        trace = []
        ex.lower_bound(ex.CATALOGUE, 95, trace)
        self.assertEqual(len(trace), 3)
        trace = []
        ex.lower_bound(ex.CATALOGUE, 5, trace)
        self.assertEqual(len(trace), 4)
        for n in range(0, 200):
            a = list(range(0, 2 * n, 2))
            looks = set()
            for key in range(-1, 2 * n + 1):
                trace = []
                ex.lower_bound(a, key, trace)
                looks.add(len(trace))
            self.assertEqual(min(looks), int(math.log2(n + 1)))
            self.assertEqual(max(looks), n.bit_length())

    def test_inclusive_hi_bug(self) -> None:
        """Thinking Problem 3: with hi = n - 1 the answer can never be n, so [12] and key 25 gives 0, not 1."""
        def buggy(a, key):
            lo, hi = 0, len(a) - 1
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid] < key:
                    lo = mid + 1
                else:
                    hi = mid
            return lo
        self.assertEqual((buggy([12], 25), ex.lower_bound([12], 25)), (0, 1))
        self.assertEqual((buggy(ex.CATALOGUE, 95), ex.lower_bound(ex.CATALOGUE, 95)), (11, 12))


if __name__ == "__main__":
    unittest.main()
