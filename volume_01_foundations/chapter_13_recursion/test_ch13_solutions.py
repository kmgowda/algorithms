import math
import random
import unittest

import ch13_solutions as sol


class TestChapter13Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        with self.assertRaises(ValueError):
            sol.largest_of([])
        self.assertEqual(sol.largest_of([47]), 47)
        self.assertEqual(sol.largest_of([12, 91]), 91)
        self.assertEqual(sol.largest_of([91, 12]), 91)
        self.assertEqual(sol.largest_of([91, 91]), 91)
        self.assertEqual(sol.largest_split_costs(1), (0, 1))

    def test_shelf(self) -> None:
        shelf = [12, 25, 31, 47, 58, 63, 70, 84, 91]
        self.assertEqual(sol.largest_of(shelf), 91)
        self.assertEqual(sol.largest_of(shelf[::-1]), 91)
        self.assertEqual(sol.largest_split_costs(9), (8, 5))

    def test_long_list_has_shallow_recursion(self) -> None:
        self.assertEqual(sol.largest_of(list(range(5000))), 4999)     # the one-item-at-a-time largest fails here
        self.assertEqual(sol.largest_split_costs(2000), (1999, 12))

    def test_against_brute_force(self) -> None:
        rng = random.Random(13)
        for _ in range(500):
            xs = [rng.randint(-20, 20) for _ in range(rng.randint(1, 40))]
            self.assertEqual(sol.largest_of(xs), max(xs))
        for n in range(1, 600):
            self.assertEqual(sol.largest_split_costs(n), (n - 1, math.ceil(math.log2(n)) + 1))


if __name__ == "__main__":
    unittest.main()
