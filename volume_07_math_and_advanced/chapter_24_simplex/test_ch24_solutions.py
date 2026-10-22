import unittest
from fractions import Fraction

import ch24_examples as ex
from ch24_solutions import cost_range


class TestCostRange(unittest.TestCase):
    def test_library(self) -> None:
        self.assertEqual(cost_range(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C, 0), (2, 4))
        self.assertEqual(cost_range(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C, 1), (Fraction(3, 2), 3))
        for c1 in (Fraction(21, 10), 3, Fraction(39, 10)):
            self.assertEqual(ex.simplex(ex.LIBRARY_A, ex.LIBRARY_B, [c1, 2])["x"], [30, 20])
        self.assertEqual(ex.simplex(ex.LIBRARY_A, ex.LIBRARY_B, [Fraction(41, 10), 2])["x"], [40, 0])

    def test_not_made_and_smallest(self) -> None:
        self.assertEqual(cost_range([[1, 1]], [4], [3, 1], 1), (None, 3))      # y is not made until it earns 3
        self.assertEqual(cost_range([[1]], [5], [2], 0), (0, None))            # one item: any rate >= 0 keeps it
        self.assertIsNone(cost_range([[1, -1]], [2], [1, 1], 0))               # unbounded: no best plan


if __name__ == "__main__":
    unittest.main()
