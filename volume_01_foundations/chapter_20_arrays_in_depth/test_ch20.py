import unittest

import ch20_examples as ex


class TestChapter20(unittest.TestCase):
    def test_grid(self) -> None:
        self.assertEqual(ex.address(1, 3, 5), 1008)
        self.assertEqual(ex.address(2, 2, 5), 1012)
        self.assertEqual(sorted(ex.neighbours(1, 3, 3, 5)), [(0, 3), (1, 2), (1, 4), (2, 3)])
        self.assertEqual(sorted(ex.neighbours(0, 0, 3, 5)), [(0, 1), (1, 0)])
        self.assertEqual(sorted(ex.neighbours(2, 4, 3, 5)), [(1, 4), (2, 3)])
        self.assertEqual(ex.totals(ex.SEATS), ([2, 3, 2], [1, 1, 2, 1, 2]))
        self.assertEqual(ex.lonely_seats(ex.SEATS), [(0, 1), (0, 4), (1, 0), (2, 4)])
        g = ex.make_grid(3, 5)
        g[0][0] = 1
        self.assertEqual([row[0] for row in g], [1, 0, 0])


if __name__ == "__main__":
    unittest.main()
