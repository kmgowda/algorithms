import unittest
from fractions import Fraction

from ch23_solutions import largest_table


class TestLargestTable(unittest.TestCase):
    def test_room(self) -> None:
        self.assertEqual(largest_table([[1, 0], [0, 1], [3, 4]], [8, 6, 36]), (3, 3, 3))

    def test_square_and_strip(self) -> None:
        self.assertEqual(largest_table([[1, 0], [0, 1]], [4, 4]), (2, 2, 2))
        x, y, r = largest_table([[1, 0], [0, 1]], [10, 2])
        self.assertEqual((y, r), (1, 1))
        self.assertTrue(1 <= x <= 9)

    def test_smallest(self) -> None:
        self.assertEqual(largest_table([[1, 0], [0, 1]], [0, 5])[2], 0)      # a room of zero width
        self.assertIsNone(largest_table([[1, 0]], [-1]))                       # no room at all
        self.assertEqual(largest_table([[1, 1]], [2])[2], Fraction(2) / (2 + Fraction(2 ** 0.5)))


if __name__ == "__main__":
    unittest.main()
