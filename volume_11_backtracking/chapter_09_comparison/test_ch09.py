import itertools
import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestComparison(unittest.TestCase):
    def test_methods_agree(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            vals = [rng.randint(1, 30) for _ in range(rng.randint(0, 12))]
            t = rng.randint(0, 120)
            truth = ex.subset_sum_brute(vals, t)[0]
            self.assertEqual(ex.subset_sum_backtrack(vals, t)[0], truth)
            self.assertEqual(ex.subset_sum_meet_in_middle(vals, t), truth)
            count = sum(1 for r in range(len(vals) + 1) for c in itertools.combinations(vals, r) if sum(c) == t)
            self.assertEqual(sol.meet_in_middle_count(vals, t), count)

    def test_examples(self) -> None:
        vals = [62, 94, 36, 104, 52, 78, 28, 122, 46, 90, 74, 58, 110, 24, 82, 66, 40, 116]
        brute = ex.subset_sum_brute(vals, 641)
        back = ex.subset_sum_backtrack(vals, 641)
        self.assertEqual(brute, (False, 2 ** 18))
        self.assertLess(back[1], brute[1])
        picks = sol.pick_methods()
        self.assertEqual(picks["fill a crossword grid"], "backtracking")
        self.assertEqual(picks["cheapest delivery round for 15 stops"], "branch-and-bound")
        self.assertEqual(ex.choose_search(set()), "brute force baseline, then look for structure")


if __name__ == "__main__":
    unittest.main()
