import random
import unittest

import ch08_solutions as sol


def brute(xs, k):
    sums = [sum(xs[i:i + k]) for i in range(len(xs) - k + 1)]
    return sums.index(max(sums)), max(sums)


class TestChapter8Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.busiest_stretch([7], 1), (0, 7))
        self.assertEqual(sol.busiest_stretch([3, 5], 1), (1, 5))
        self.assertEqual(sol.busiest_stretch([3, 5], 2), (0, 8))
        self.assertEqual(sol.busiest_stretch([4, 4, 4], 2), (0, 8))
        self.assertEqual(sol.busiest_stretch([-5, -2, -9], 1), (1, -2))

    def test_week(self) -> None:
        week = [34, 41, 29, 56, 48, 61, 22]
        self.assertEqual(sol.busiest_stretch(week, 3), (3, 165))
        self.assertEqual(sol.busiest_stretch(week, 1), (5, 61))
        self.assertEqual(sol.busiest_stretch(week, 7), (0, 291))

    def test_against_brute_force(self) -> None:
        rng = random.Random(8)
        for _ in range(500):
            xs = [rng.randint(-20, 60) for _ in range(rng.randint(1, 15))]
            k = rng.randint(1, len(xs))
            self.assertEqual(sol.busiest_stretch(xs, k), brute(xs, k))


if __name__ == "__main__":
    unittest.main()
