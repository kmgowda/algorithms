import random
import unittest

import ch10_solutions as sol


class TestChapter7Solutions(unittest.TestCase):
    def test_dual_pivot_partition(self) -> None:
        a, c = list(sol.PILE), {"comparisons": 0}
        self.assertEqual(sol.dual_pivot_partition(a, 0, 8, c), (4, 5))
        self.assertEqual(a, [47, 25, 31, 12, 58, 63, 70, 91, 84])
        self.assertEqual(c["comparisons"], 11)
        b = [5, 1]
        self.assertEqual(sol.dual_pivot_partition(b, 0, 1), (0, 1))
        self.assertEqual(b, [1, 5])
        rng = random.Random(8)
        for _ in range(500):
            m = rng.randint(2, 20)
            x = [rng.randint(0, 9) for _ in range(m)]
            y, c = list(x), {"comparisons": 0}
            l, g = sol.dual_pivot_partition(y, 0, m - 1, c)
            self.assertEqual(sorted(y), sorted(x))
            p, q = y[l], y[g]
            self.assertTrue(all(v < p for v in y[:l]))
            self.assertTrue(all(p <= v <= q for v in y[l + 1:g]))
            self.assertTrue(all(v > q for v in y[g + 1:]))
            self.assertLessEqual(c["comparisons"], 2 * (m - 2) + 1)

    def test_dual_pivot_quicksort(self) -> None:
        for x in ([], [7], [2, 1], [7] * 9, list(sol.PILE)):
            y = list(x)
            sol.dual_pivot_quicksort(y)
            self.assertEqual(y, sorted(x))
        rng = random.Random(9)
        for _ in range(300):
            x = [rng.randint(0, rng.choice([3, 60])) for _ in range(rng.randint(0, 50))]
            y = list(x)
            sol.dual_pivot_quicksort(y)
            self.assertEqual(y, sorted(x))
        c = {"comparisons": 0}
        sol.dual_pivot_quicksort([7] * 4000, counter=c)
        self.assertEqual(c["comparisons"], 7997)
        rng = random.Random(1)
        a, c = [rng.random() for _ in range(1000)], {"comparisons": 0}
        sol.dual_pivot_quicksort(a, counter=c)
        self.assertEqual(c["comparisons"], 10667)

    def test_buggy_partition3(self) -> None:
        b = [2, 3, 1]
        self.assertEqual(sol.partition3_buggy(b, 0, 2, 2), (0, 1))
        self.assertEqual(b, [2, 1, 3])                      # 1 is claimed to equal the pivot 2

    def test_hoare_split(self) -> None:
        self.assertEqual(sol.hoare_returns([12, 25], 0, 1, middle=False), 1)   # j = hi: no progress
        self.assertEqual(sol.hoare_returns([12, 25], 0, 1), 0)
        rng = random.Random(2)
        for _ in range(5000):
            n = rng.randint(2, 12)
            y = [rng.randint(0, 5) for _ in range(n)]
            j = sol.hoare_returns(y, 0, n - 1)
            self.assertTrue(0 <= j < n - 1)
            self.assertLessEqual(max(y[:j + 1]), min(y[j + 1:]))


if __name__ == "__main__":
    unittest.main()
