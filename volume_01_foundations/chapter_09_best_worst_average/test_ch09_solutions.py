import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestChapter9Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.day_summary([], []), (0, 0, 0.0))
        self.assertEqual(sol.day_summary([], [5, 7]), (0, 0, 0.0))
        self.assertEqual(sol.day_summary(sol.SHELF, []), (0, 0, 0.0))
        self.assertEqual(sol.day_summary([47], [47]), (1, 1, 1.0))
        self.assertEqual(sol.day_summary([47], [12]), (1, 1, 1.0))
        self.assertEqual(sol.day_summary([5, 5], [5]), (1, 1, 1.0))      # the first copy is found

    def test_example(self) -> None:
        self.assertEqual(sol.day_summary(sol.SHELF, [12, 91, 50, 63]), (1, 9, 6.25))
        self.assertEqual(sol.day_summary(sol.SHELF, sol.SHELF), (1, 9, 5.0))

    def test_against_brute_force(self) -> None:
        rng = random.Random(9)
        for _ in range(500):
            shelf = [rng.randint(0, 15) for _ in range(rng.randint(0, 10))]
            requests = [rng.randint(0, 17) for _ in range(rng.randint(1, 12))]
            costs = [ex.looks(shelf, t) for t in requests]
            best, worst, avg = sol.day_summary(shelf, requests)
            self.assertEqual((best, worst), (min(costs), max(costs)))
            self.assertAlmostEqual(avg, sum(costs) / len(costs))


if __name__ == "__main__":
    unittest.main()
