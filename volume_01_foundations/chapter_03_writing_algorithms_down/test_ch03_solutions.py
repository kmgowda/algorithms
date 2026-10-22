import random
import unittest

import ch03_solutions as sol


class TestChapter3Solutions(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertIsNone(sol.smallest_gap([]))
        self.assertIsNone(sol.smallest_gap([47]))
        self.assertEqual(sol.smallest_gap([47, 58]), (11, 47, 58))
        self.assertEqual(sol.smallest_gap([5, 5, 9]), (0, 5, 5))

    def test_shelf(self) -> None:
        self.assertEqual(sol.smallest_gap(sol.SHELF), (5, 58, 63))

    def test_against_every_pair(self) -> None:
        rng = random.Random(3)
        for _ in range(500):
            xs = sorted(rng.randint(0, 100) for _ in range(rng.randint(2, 12)))
            brute = min(xs[j] - xs[i] for i in range(len(xs)) for j in range(i + 1, len(xs)))
            gap, a, b = sol.smallest_gap(xs)
            self.assertEqual(gap, brute)
            self.assertEqual(b - a, gap)


if __name__ == "__main__":
    unittest.main()
