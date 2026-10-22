import random
import unittest

import ch06_solutions as sol


class TestChapter6Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertFalse(sol.has_duplicate([], 0))
        self.assertFalse(sol.has_duplicate([0], 0))
        self.assertTrue(sol.has_duplicate([0, 0], 0))
        self.assertFalse(sol.has_duplicate([3, 5], 5))
        self.assertTrue(sol.has_duplicate([5, 3, 5], 5))

    def test_shelf(self) -> None:
        shelf = [12, 25, 31, 47, 58, 63, 70, 84, 91]
        self.assertFalse(sol.has_duplicate(shelf, 100))
        self.assertTrue(sol.has_duplicate(shelf + [47], 100))

    def test_against_every_pair(self) -> None:
        rng = random.Random(6)
        for _ in range(500):
            k = rng.randint(0, 12)
            xs = [rng.randint(0, k) for _ in range(rng.randint(0, 10))]
            brute = any(xs[i] == xs[j] for i in range(len(xs)) for j in range(i + 1, len(xs)))
            self.assertEqual(sol.has_duplicate(xs, k), brute)

    def test_hidden_comparisons(self) -> None:
        self.assertEqual([sol.hidden_comparisons(list(range(n))) for n in (0, 1, 2, 3, 4)], [0, 0, 1, 3, 6])
        self.assertEqual(sol.hidden_comparisons([12, 25, 31, 47]), 6)
        self.assertEqual(sol.hidden_comparisons(list(range(1000))), 499_500)
        self.assertEqual(sol.hidden_comparisons(list(range(2000))), 1_999_000)
        self.assertEqual(sol.hidden_comparisons([7, 7, 7]), 2)


if __name__ == "__main__":
    unittest.main()
