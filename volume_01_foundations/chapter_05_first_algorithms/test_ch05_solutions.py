import random
import unittest

import ch05_solutions as sol


class TestChapter5Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.min_and_max([7]), (7, 7, 0))
        self.assertEqual(sol.min_and_max([3, 5]), (3, 5, 1))
        self.assertEqual(sol.min_and_max([5, 3]), (3, 5, 1))
        self.assertEqual(sol.min_and_max([4, 4]), (4, 4, 1))
        self.assertEqual(sol.min_and_max([2, 9, 1]), (1, 9, 3))

    def test_busiest_week(self) -> None:
        self.assertEqual(sol.min_and_max([34, 41, 29, 56, 48, 61, 22]), (22, 61, 9))
        self.assertEqual(sol.min_and_max([142, 155, 138, 161, 150, 158]), (138, 161, 7))

    def test_against_brute_force(self) -> None:
        rng = random.Random(5)
        for _ in range(500):
            xs = [rng.randint(-20, 20) for _ in range(rng.randint(1, 15))]
            least, best, comps = sol.min_and_max(xs)
            self.assertEqual((least, best), (min(xs), max(xs)))
            n = len(xs)
            self.assertEqual(comps, 3 * (n - 1) // 2 if n % 2 else 3 * n // 2 - 2)
            self.assertLessEqual(comps, 2 * (n - 1))


if __name__ == "__main__":
    unittest.main()
