import random
import unittest

import ch14_examples as ex
import ch14_solutions as sol


class TestChapter14Solutions(unittest.TestCase):
    def test_known_sets(self) -> None:
        self.assertEqual(sol.is_canonical(ex.UK), (True, None))
        self.assertEqual(sol.is_canonical(ex.ODD), (False, 6))
        self.assertEqual(sol.is_canonical([1, 5]), (True, None))
        self.assertEqual(sol.is_canonical([1, 5, 8]), (False, 10))     # Thinking Problem 1
        self.assertEqual(sol.is_canonical([1, 7, 10]), (False, 14))
        self.assertEqual(sol.is_canonical([25, 10, 1]), (False, 30))

    def test_smallest(self) -> None:
        self.assertEqual(sol.is_canonical([1]), (True, None))
        self.assertEqual(sol.is_canonical([1, 2]), (True, None))
        with self.assertRaises(ValueError):
            sol.is_canonical([2, 5])
        with self.assertRaises(ValueError):
            sol.is_canonical([])

    def test_random_against_search(self) -> None:
        rng = random.Random(14)
        for _ in range(300):
            coins = sorted({1, *rng.sample(range(2, 30), rng.randint(1, 4))})
            self.assertEqual(sol.is_canonical(coins)[1], ex.first_failure(coins, 120))


if __name__ == "__main__":
    unittest.main()
