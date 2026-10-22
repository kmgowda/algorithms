import random
import unittest

import ch17_examples as ex
import ch17_solutions as sol


class TestChapter14Thinking(unittest.TestCase):
    def test_mom_bad_input(self) -> None:
        for m, smaller in [(1, 2), (3, 5), (5, 8), (25, 38), (201, 302)]:
            a = sol.mom_bad_input(m)
            _, p = ex.mom_pivot(a)
            self.assertEqual(sum(x < p for x in a), smaller)
            self.assertEqual(smaller, 3 * (m + 1) // 2 - 1)
            self.assertGreaterEqual(smaller, ex.guaranteed_side(5 * m))
        a = sol.mom_bad_input(5)
        self.assertLess(sum(x < 10 ** 6 for x in a), 2 * len(a) / 5)
        with self.assertRaises(ValueError):
            sol.mom_bad_input(4)

    def test_weighted_median_small(self) -> None:
        self.assertEqual(sol.weighted_median([47], [5]), 47)
        self.assertEqual(sol.weighted_median([30, 10], [1, 1]), 10)
        self.assertEqual(sol.weighted_median([30, 10], [1, 2]), 10)
        self.assertEqual(sol.weighted_median([30, 10], [3, 1]), 30)
        self.assertEqual(sol.weighted_median([47, 47, 12], [1, 1, 1]), 47)
        with self.assertRaises(ValueError):
            sol.weighted_median([], [])
        with self.assertRaises(ValueError):
            sol.weighted_median([1], [0])

    def test_weighted_median_corridor(self) -> None:
        w = dict(zip([12, 25, 31, 47, 58, 63, 70, 84, 91], [3, 1, 4, 1, 5, 9, 2, 6, 5]))
        weights = [w[x] for x in ex.PILE]
        self.assertEqual(sol.weighted_median(ex.PILE, weights), 63)
        cost = lambda c: sum(wt * abs(c - x) for x, wt in w.items())  # noqa: E731
        self.assertEqual(min(w, key=cost), 63)
        self.assertEqual(cost(63), 640)
        self.assertEqual(cost(58), 680)

    def test_weighted_median_random(self) -> None:
        rng = random.Random(3)
        for _ in range(500):
            n = rng.randint(1, 30)
            items = [rng.randint(0, 20) for _ in range(n)]
            weights = [rng.randint(1, 9) for _ in range(n)]
            want = sol.weighted_median_by_sorting(items, weights)
            self.assertEqual(sol.weighted_median(items, weights, random.Random(n)), want)
            unit = sol.weighted_median(items, [1] * n)
            self.assertEqual(unit, sorted(items)[(n + 1) // 2 - 1])

    def test_buggy_two_way_select(self) -> None:
        self.assertEqual(sol.first_pivot_select_buggy(ex.PILE, 5, 6), (None, [9, 5, 5, 5, 5, 5]))
        self.assertEqual(sol.first_pivot_select_buggy([12, 25, 31], 1, 4), (None, [3, 3, 3, 3]))
        self.assertEqual(sol.first_pivot_select_buggy([47] * 9, 5, 3), (None, [9, 9, 9]))
        self.assertEqual(sol.first_pivot_select_buggy([47], 1), (47, [1]))
        self.assertEqual(sol.first_pivot_select_buggy([31, 25, 12], 1)[0], 12)
        for a, k in [(ex.PILE, 5), ([12, 25, 31], 1), ([47] * 9, 5)]:
            self.assertEqual(ex.median_of_medians(a, k), sorted(a)[k - 1])


if __name__ == "__main__":
    unittest.main()
