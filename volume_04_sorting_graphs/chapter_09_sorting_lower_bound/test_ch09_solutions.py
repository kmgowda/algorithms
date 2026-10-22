import itertools
import math
import random
import unittest
from collections import Counter

import ch09_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_merge_needs_2n_minus_1(self) -> None:          # Thinking Problem 1
        self.assertEqual(sol.optimal_merge_comparisons(0, 3), 0)
        self.assertEqual(sol.optimal_merge_comparisons(1, 1), 1)
        self.assertEqual([sol.merge_counting_bound(n, n) for n in (1, 2, 3, 4, 5, 8)], [1, 3, 5, 7, 8, 14])
        for n in range(1, 6):
            self.assertEqual(sol.optimal_merge_comparisons(n, n), 2 * n - 1)
        self.assertEqual(sol.optimal_merge_comparisons(1, 3), 2)  # unequal shelves: binary insertion of one book

    def test_sort_few_distinct(self) -> None:                 # Thinking Problem 2
        self.assertEqual(sol.sort_few_distinct([]), ([], 0))
        self.assertEqual(sol.sort_few_distinct([7]), ([7], 0))
        self.assertEqual(sol.sort_few_distinct([7, 7, 7]), ([7, 7, 7], 4))
        self.assertEqual(sol.sort_few_distinct([58, 25, 58, 12, 25, 47, 58, 12, 47]),
                         ([12, 12, 25, 25, 47, 47, 58, 58, 58], 24))
        rng = random.Random(1)
        for _ in range(200):
            k = rng.randint(1, 8)
            a = [rng.randint(0, k - 1) for _ in range(rng.randint(0, 60))]
            out, comps = sol.sort_few_distinct(a)
            self.assertEqual(out, sorted(a))
            self.assertLessEqual(comps, sol.few_distinct_bound(len(a), len(set(a))))
        loans = random.Random(1)
        a = [loans.randint(0, 5) for _ in range(1000)]
        out, comps = sol.sort_few_distinct(a)
        self.assertEqual((comps, sol.few_distinct_bound(1000, 6)), (3988, 4000))
        arrangements = math.factorial(1000)
        for c in Counter(a).values():
            arrangements //= math.factorial(c)
        self.assertEqual((arrangements - 1).bit_length(), 2560)  # the counting bound for this multiset

    def test_five_books(self) -> None:                         # Thinking Problem 3
        self.assertEqual(sol.rosa_sort5((31, 47, 12, 58, 25)), ([12, 25, 31, 47, 58], 8))
        self.assertEqual(sol.ford_johnson5((31, 47, 12, 58, 25)), ([12, 25, 31, 47, 58], 7))
        self.assertEqual(sol.worst_over_orders(sol.rosa_sort5)[0], 8)
        self.assertEqual(sol.worst_over_orders(sol.ford_johnson5)[0], 7)
        bad = [p for p in itertools.permutations((12, 25, 31, 47, 58)) if sol.rosa_sort5(p)[1] == 8]
        self.assertEqual(len(bad), 32)
        for p in itertools.product((1, 2), repeat=5):             # equal books are sorted too
            self.assertEqual(sol.ford_johnson5(p)[0], sorted(p))
            self.assertEqual(sol.rosa_sort5(p)[0], sorted(p))


if __name__ == "__main__":
    unittest.main()
