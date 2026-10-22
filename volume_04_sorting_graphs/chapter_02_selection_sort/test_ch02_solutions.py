import itertools
import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


def buggy_double_selection(a):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        small = large = lo
        for k in range(lo + 1, hi + 1):
            if a[k] < a[small]:
                small = k
            if a[k] > a[large]:
                large = k
        a[lo], a[small] = a[small], a[lo]
        a[hi], a[large] = a[large], a[hi]
        lo, hi = lo + 1, hi - 1
    return a


class TestChapter02Solutions(unittest.TestCase):
    def test_swaps_are_n_minus_cycles(self) -> None:          # Thinking Problem 1
        self.assertEqual(sol.cycle_count(sol.PILE), 2)
        self.assertEqual(sol.cycle_count([]), 0)
        rng = random.Random(1)
        for _ in range(300):
            a = rng.sample(range(100), rng.randint(0, 15))
            self.assertEqual(ex.selection_sort(list(a))["swaps"], len(a) - sol.cycle_count(a))

    def test_swap_plan(self) -> None:          # Thinking Problem 2
        self.assertEqual(sol.crate_swap_plan([]), [])
        self.assertEqual(sol.crate_swap_plan([5]), [])
        self.assertEqual(sol.crate_swap_plan([1, 2, 3]), [])
        self.assertEqual(sol.crate_swap_plan([2, 1]), [(0, 1)])
        self.assertEqual(len(sol.crate_swap_plan(sol.PILE)), 7)
        self.assertEqual(len(sol.crate_swap_plan(sorted(sol.PILE, reverse=True))), 4)
        rng = random.Random(2)
        for _ in range(300):
            a = [rng.randint(0, 9) for _ in range(rng.randint(0, 15))]          # duplicates allowed
            plan = sol.crate_swap_plan(a)
            self.assertEqual(sol.apply_plan(a, plan), sorted(a))
            if len(set(a)) == len(a):
                self.assertEqual(len(plan), ex.selection_sort(list(a))["swaps"])

    def test_double_selection(self) -> None:          # Thinking Problem 3
        self.assertEqual(buggy_double_selection([2, 1]), [2, 1])
        self.assertEqual(buggy_double_selection([3, 1, 2]), [2, 3, 1])
        self.assertEqual(buggy_double_selection(list(sol.PILE)), sorted(sol.PILE))
        for a in ([], [1], [2, 1], [1, 1], [47] * 9):
            b = list(a)
            sol.double_selection_sort(b)
            self.assertEqual(b, sorted(a))
        for n in range(7):
            for p in itertools.permutations(range(n)):
                b = list(p)
                sol.double_selection_sort(b)
                self.assertEqual(b, list(range(n)))


if __name__ == "__main__":
    unittest.main()
