import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestTesting(unittest.TestCase):
    def test_tools(self) -> None:
        rng = random.Random(1)
        self.assertIsNone(ex.find_counterexample(ex.max_profit, ex.max_profit_brute, 2000, rng))
        bad = ex.find_counterexample(ex.max_profit_buggy, ex.max_profit_brute, 2000, rng)
        self.assertIsNotNone(bad)
        fails = lambda c: ex.max_profit_buggy(c) != ex.max_profit_brute(c)
        small = ex.shrink(bad, fails)
        self.assertTrue(fails(small))
        self.assertTrue(all(not fails(small[:i] + small[i + 1:]) for i in range(len(small))))
        self.assertEqual(len(small), 3)
        for c in ex.edge_cases_for_list():
            self.assertEqual(ex.max_profit(c), ex.max_profit_brute(c))
        self.assertEqual(ex.max_profit_brute([8, 5]), 0)
        self.assertEqual(ex.debug_report([3, 1, 4])[-1], "day 2: price 4, cheapest 1, best 3")

    def test_solutions(self) -> None:
        rng = random.Random(2)
        for _ in range(300):
            nums = sorted(rng.sample(range(30), rng.randint(0, 10)))
            t = rng.randint(0, 30)
            self.assertEqual(sol.binary_search_fixed(nums, t), nums.index(t) if t in nums else -1)
        self.assertIn("", sol.edge_cases_for_string())
        self.assertIn(["1"], sol.edge_cases_for_grid())


if __name__ == "__main__":
    unittest.main()
