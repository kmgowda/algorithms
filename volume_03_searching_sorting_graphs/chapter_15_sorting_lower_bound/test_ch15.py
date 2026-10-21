import itertools
import math
import unittest

import ch15_examples as ex


class TestChapter15(unittest.TestCase):
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
