import itertools
import math
import unittest

import ch07_solutions as sol


def brute(n, k, c):
    return sum(1 for combo in itertools.combinations_with_replacement(range(n), k)
               if all(combo.count(x) <= c for x in range(n)))


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual((sol.bounded_choices(0, 0, 3), sol.bounded_choices(0, 2, 3)), (1, 0))
        self.assertEqual((sol.bounded_choices(3, 0, 0), sol.bounded_choices(3, 1, 0)), (1, 0))
        self.assertEqual(sol.bounded_choices(1, 1, 1), 1)

    def test_bookmarks(self) -> None:
        self.assertEqual(sol.bounded_choices(3, 4, 2), 6)
        self.assertEqual(sol.bounded_choices(3, 4, 4), 15)          # no real limit: stars and bars

    def test_against_listing(self) -> None:
        for n in range(0, 6):
            for k in range(0, 8):
                for c in range(0, 5):
                    self.assertEqual(sol.bounded_choices(n, k, c), brute(n, k, c), (n, k, c))

    def test_overcount(self) -> None:
        self.assertEqual(sol.at_least_one_overcount(5, 5, 3), 180)
        self.assertEqual(math.comb(10, 3) - math.comb(5, 3), 110)
        self.assertEqual(sol.at_least_one_overcount(2, 1, 2), 4)

    def test_odd_entries(self) -> None:
        for n in range(200):
            self.assertEqual(sol.odd_entries(n), 2 ** bin(n).count("1"))


if __name__ == "__main__":
    unittest.main()
