import itertools
import math
import unittest

import ch09_examples as ex


class TestChapter15(unittest.TestCase):
    def test_average_case(self) -> None:                      # Section 9.6, Figure 9.4
        import math
        self.assertAlmostEqual(ex.average_depth_sort3(), 8 / 3)
        self.assertEqual([ex.min_total_leaf_depth(k) for k in range(0, 7)], [0, 0, 2, 5, 8, 12, 16])
        self.assertAlmostEqual(ex.average_lower_bound(3), 8 / 3)
        self.assertAlmostEqual(ex.average_lower_bound(4), 112 / 24)
        self.assertEqual(ex.average_lower_bound(1), 0)
        for n in range(2, 9):
            self.assertGreaterEqual(ex.average_lower_bound(n), math.log2(math.factorial(n)) - 1e-9)
        for leaves in range(1, 40):           # balanced trees: brute force over all splits of the leaves
            best = {1: 0}
            for k in range(2, leaves + 1):
                best[k] = min(best[i] + best[k - i] + k for i in range(1, k))
            self.assertEqual(ex.min_total_leaf_depth(leaves), best[leaves])

    def test_distinctness(self) -> None:
        self.assertEqual(ex.all_distinct_by_sorting([58, 25, 91, 12, 70, 47, 84, 31, 63]), (True, 29))
        self.assertFalse(ex.all_distinct_by_sorting([58, 25, 58])[0])
        self.assertEqual(ex.all_distinct_by_sorting([]), (True, 0))
        self.assertEqual(ex.all_distinct_by_sorting([7]), (True, 0))

    def test_every_case(self) -> None:
        rows = ex.every_order_of_three()
        self.assertEqual([r[1] for r in rows], [2, 3, 2, 3, 3, 3])
        for perm in itertools.product((1, 2), repeat=3):          # equal keys too
            self.assertEqual(list(ex.sort3(*perm)), sorted(perm))

    def test_bound(self) -> None:
        self.assertEqual([ex.lower_bound(n) for n in (1, 2, 3, 4, 5, 9, 100, 1000)], [0, 1, 3, 5, 7, 19, 525, 8530])
        for n in range(2, 300):
            self.assertGreaterEqual(2 ** ex.lower_bound(n), math.factorial(n))
            self.assertLess(2 ** (ex.lower_bound(n) - 1), math.factorial(n))
            self.assertGreaterEqual(ex.merge_sort_worst(n), ex.lower_bound(n))

    def test_merge_worst_formula(self) -> None:
        for n in range(1, 8):
            self.assertEqual(max(ex.merge_comparisons(p) for p in itertools.permutations(range(n))), ex.merge_sort_worst(n))


if __name__ == "__main__":
    unittest.main()
