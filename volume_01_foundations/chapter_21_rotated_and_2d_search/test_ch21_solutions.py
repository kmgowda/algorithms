import random
import unittest

import ch21_solutions as sol


class TestChapter21Solutions(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(sol.count_in_range_rotated(sol.ROTATED, 30, 70), 5)
        self.assertEqual(sol.count_in_range_rotated(sol.ROTATED, 0, 100), 9)
        self.assertEqual(sol.count_in_range_rotated(sol.ROTATED, 64, 69), 0)

    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.count_in_range_rotated([], 0, 10), 0)
        self.assertEqual(sol.count_in_range_rotated([5], 5, 5), 1)
        self.assertEqual(sol.count_in_range_rotated([5], 6, 9), 0)
        self.assertEqual(sol.count_in_range_rotated([25, 12], 12, 12), 1)
        self.assertEqual(sol.count_in_range_rotated([25, 12], 20, 10), 0)   # empty range

    def test_against_brute_force(self) -> None:
        rng = random.Random(21)
        for _ in range(400):
            base = sorted(rng.sample(range(60), rng.randint(0, 12)))
            k = rng.randrange(len(base)) if base else 0
            a = base[k:] + base[:k]
            low = rng.randint(-2, 62)
            high = rng.randint(low - 3, 63)
            self.assertEqual(sol.count_in_range_rotated(a, low, high), sum(low <= v <= high for v in a))


if __name__ == "__main__":
    unittest.main()
