import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestComparison(unittest.TestCase):
    def test_methods_agree(self) -> None:
        rng = random.Random(1)
        for _ in range(100):
            coins = tuple(sorted(set([1] + rng.sample(range(2, 12), rng.randint(0, 3)))))
            amount = rng.randint(0, 20)
            d = ex.change_dynamic(amount, coins)
            self.assertEqual(ex.change_plain_recursion(amount, coins), d)
            self.assertEqual(ex.change_backtracking(amount, coins), d)
            self.assertGreaterEqual(ex.change_greedy(amount, coins), d)
        self.assertIsNone(ex.change_dynamic(3, (2,)))
        self.assertIsNone(ex.change_backtracking(3, (2,)))

    def test_race_and_solutions(self) -> None:
        r = ex.race(25, (1, 3, 4))
        self.assertLess(r["dynamic programming"], r["plain recursion"])
        picks = sol.classify_problems()
        self.assertEqual(picks["most talks in one hall"], "greedy")
        self.assertEqual(picks["fill a sudoku"], "backtracking")
        calls = [sol.count_calls_plain(n, (1, 3, 4)) for n in (5, 10, 15)]
        self.assertTrue(calls[0] < calls[1] < calls[2])
        self.assertEqual(ex.choose_paradigm(set()), "brute force baseline first")


if __name__ == "__main__":
    unittest.main()
