import random
import unittest

import ch18_examples as ex
import ch18_solutions as sol

SHELF = [4, 6, 9, 13, 15, 17, 20]


def brute_best(prices: list[int], target: int) -> int | None:
    """The largest total of two different books that does not go over target, trying every pair."""
    totals = [prices[i] + prices[j] for i in range(len(prices)) for j in range(i + 1, len(prices))
              if prices[i] + prices[j] <= target]
    return max(totals) if totals else None


class TestChapter18Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertIsNone(sol.best_pair_at_most([], 10))
        self.assertIsNone(sol.best_pair_at_most([5], 10))
        self.assertEqual(sol.best_pair_at_most([5, 5], 10), (0, 1))
        self.assertIsNone(sol.best_pair_at_most([5, 6], 10))

    def test_display_shelf(self) -> None:
        self.assertEqual(sol.best_pair_at_most(SHELF, 27), (1, 6))
        self.assertEqual(sol.best_pair_at_most(SHELF, 30), (3, 5))
        self.assertEqual(sol.best_pair_at_most(SHELF, 10), (0, 1))
        self.assertIsNone(sol.best_pair_at_most(SHELF, 9))
        self.assertEqual(sol.best_pair_at_most(SHELF, 100), (5, 6))

    def test_against_brute_force(self) -> None:
        rng = random.Random(18)
        for _ in range(2000):
            prices = sorted(rng.randint(1, 30) for _ in range(rng.randint(0, 10)))
            target = rng.randint(0, 65)
            got = sol.best_pair_at_most(prices, target)
            expected = brute_best(prices, target)
            if expected is None:
                self.assertIsNone(got)
            else:
                i, j = got
                self.assertLess(i, j)
                self.assertEqual(prices[i] + prices[j], expected)

    def test_widest_pair(self) -> None:
        """Thinking Problem 1: two pointers return the valid pair whose positions enclose every other valid pair."""
        self.assertEqual(ex.pair_two_pointers(SHELF, 24), (0, 6))
        rng = random.Random(181)
        for _ in range(20000):
            prices = sorted(rng.randint(1, 30) for _ in range(rng.randint(0, 10)))
            target = rng.randint(0, 60)
            pairs = [(i, j) for i in range(len(prices)) for j in range(i + 1, len(prices))
                     if prices[i] + prices[j] == target]
            got = ex.pair_two_pointers(prices, target)
            if pairs:
                self.assertEqual(got, (min(i for i, _ in pairs), max(j for _, j in pairs)))


if __name__ == "__main__":
    unittest.main()
