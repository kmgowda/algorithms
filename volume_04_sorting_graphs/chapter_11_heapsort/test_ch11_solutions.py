import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestChapter8Solutions(unittest.TestCase):
    def test_sort_nearly_sorted(self) -> None:
        self.assertEqual(sol.sort_nearly_sorted([], 3), [])
        self.assertEqual(sol.sort_nearly_sorted([5], 0), [5])
        self.assertEqual(sol.sort_nearly_sorted([1, 2, 3], 0), [1, 2, 3])
        self.assertEqual(sol.sort_nearly_sorted([2, 1], 5), [1, 2])
        with self.assertRaises(ValueError):
            sol.sort_nearly_sorted([1], -1)
        shelf = [25, 12, 47, 31, 58, 70, 63, 91, 84]
        c = {}
        self.assertEqual(sol.max_displacement(shelf), 1)
        self.assertEqual(sol.sort_nearly_sorted(shelf, 1, c), sorted(shelf))
        self.assertEqual(c["max_heap_size"], 2)
        rng = random.Random(10)
        for _ in range(400):
            n, k = rng.randint(0, 40), rng.randint(0, 6)
            a = sorted(rng.randint(0, 20) for _ in range(n))
            for _ in range(n):                    # shuffle locally, keeping every item within k places
                p = rng.randrange(max(1, n))
                q = min(n - 1, p + rng.randint(0, k)) if n else 0
                b = a[:]
                b[p], b[q] = b[q], b[p]
                if sol.max_displacement(b) <= k:
                    a = b
            self.assertLessEqual(sol.max_displacement(a), k)
            self.assertEqual(sol.sort_nearly_sorted(a, k), sorted(a))

    def test_top_down_build_bug(self) -> None:
        self.assertEqual(sol.heapsort_top_down_build([12, 25, 31, 47]), [12, 25, 47, 31])
        a = [12, 25, 31, 47]
        for i in range(0, 2):
            ex.sift_down(a, i, 4)
        self.assertEqual(a, [31, 47, 12, 25])                # not a max-heap: 47 sits below 31

    def test_heights_sum(self) -> None:
        self.assertEqual(sol.heights_sum(0), 0)
        self.assertEqual(sol.heights_sum(1), 0)
        self.assertEqual(sol.heights_sum(9), 7)
        rng = random.Random(11)
        for n in range(1, 200):
            self.assertEqual(sol.heights_sum(n), n - bin(n).count("1"))
            a, c = [rng.random() for _ in range(n)], {"comparisons": 0}
            for i in range(n // 2 - 1, -1, -1):
                ex.sift_down(a, i, n, c)
            self.assertLessEqual(c["comparisons"], 2 * sol.heights_sum(n))


if __name__ == "__main__":
    unittest.main()
