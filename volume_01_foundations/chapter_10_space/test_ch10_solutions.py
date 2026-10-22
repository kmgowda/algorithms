import random
import unittest

import ch10_solutions as sol


class TestChapter10Solutions(unittest.TestCase):
    def check(self, xs: list[int]) -> None:
        ys = list(xs)
        k = sol.compact_sorted(ys)
        self.assertEqual(ys[:k], sorted(set(xs)))
        self.assertEqual(len(ys), len(xs))

    def test_smallest_inputs(self) -> None:
        for xs in ([], [7], [7, 7], [1, 2], [5, 5, 5, 5]):
            self.check(xs)
        self.assertEqual(sol.compact_sorted([]), 0)
        self.assertEqual(sol.compact_sorted([7, 7, 7]), 1)

    def test_example(self) -> None:
        s = list(sol.SORTED_RETURNS)
        self.assertEqual(sol.compact_sorted(s), 5)
        self.assertEqual(s[:5], [12, 25, 31, 47, 63])

    def test_against_brute_force(self) -> None:
        rng = random.Random(10)
        for _ in range(500):
            self.check(sorted(rng.randint(0, 8) for _ in range(rng.randint(0, 14))))


if __name__ == "__main__":
    unittest.main()
