import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestParadigms(unittest.TestCase):
    def test_best_stretch_three_ways(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            v = [rng.randint(-10, 10) for _ in range(rng.randint(1, 25))]
            b = ex.best_stretch_brute(v)
            self.assertEqual(ex.best_stretch_divide(v), b)
            self.assertEqual(ex.best_stretch_dynamic(v), b)

    def test_coins(self) -> None:
        rng = random.Random(2)
        for _ in range(100):
            coins = sorted(set(rng.sample(range(1, 12), rng.randint(1, 4))))
            amount = rng.randint(0, 25)
            self.assertEqual(ex.coins_dynamic(amount, coins), ex.coins_exhaustive(amount, coins))
            g = ex.coins_greedy(amount, coins)
            best = ex.coins_exhaustive(amount, coins)
            if g is not None and best is not None:
                self.assertGreaterEqual(g, best)
        self.assertEqual(ex.coins_greedy(6, [1, 3, 4]), 3)
        self.assertEqual(ex.coins_exhaustive(6, [1, 3, 4]), 2)
        self.assertEqual(ex.coins_greedy(63, [1, 5, 10, 25]), 6)

    def test_solutions(self) -> None:
        self.assertEqual(sol.find_max_divide([4, 9, 2, 7]), 9)
        self.assertEqual(sol.power_decrease(3, 13), 3 ** 13)
        self.assertTrue(sol.has_duplicates_transform([3, 1, 3]))
        self.assertFalse(sol.has_duplicates_transform([3, 1, 2]))
        self.assertEqual(sol.classify("split the list in half and merge"), "divide and conquer")
        self.assertEqual(sol.classify("remember answers to subproblems"), "dynamic programming")


if __name__ == "__main__":
    unittest.main()
