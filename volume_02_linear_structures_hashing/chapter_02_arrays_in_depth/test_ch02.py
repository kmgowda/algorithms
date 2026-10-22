import unittest

import ch02_examples as ex


class TestChapter20(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual([len(ex.neighbours(r, c, 3, 5)) for r, c in [(0, 0), (0, 2), (1, 2)]], [2, 3, 4])
        self.assertEqual((ex.neighbours(0, 0, 1, 1), ex.neighbours(0, 2, 1, 5)), ([], [(0, 1), (0, 3)]))
        self.assertEqual((ex.address(0, 0, 5), ex.address(2, 4, 5)), (1000, 1014))
        self.assertEqual(ex.totals(ex.SEATS), ([2, 3, 2], [1, 1, 2, 1, 2]))
        self.assertEqual(ex.totals([[7]]), ([7], [7]))
        self.assertEqual(ex.lonely_seats(ex.SEATS), [(0, 1), (0, 4), (1, 0), (2, 4)])
        self.assertEqual((ex.lonely_seats([[1]]), ex.lonely_seats([[1, 1]])), ([(0, 0)], []))
        bad = [[0] * 3] * 2
        bad[0][0] = 1
        good = ex.make_grid(2, 3)
        good[0][0] = 1
        self.assertEqual((bad, good), ([[1, 0, 0], [1, 0, 0]], [[1, 0, 0], [0, 0, 0]]))

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

    def test_layouts(self) -> None:
        self.assertEqual(ex.address(1, 3, 5), 1008)
        self.assertEqual(ex.address(1, 3, 5, size=8), 1064)
        self.assertEqual(ex.address(0, 0, 5, size=8), 1000)
        self.assertEqual(ex.column_major_address(1, 3, 3), 1010)
        self.assertEqual(ex.column_major_address(2, 4, 3), 1014)
        self.assertEqual(sorted({ex.address(r, c, 5) for r in range(3) for c in range(5)}), list(range(1000, 1015)))
        self.assertEqual(sorted({ex.column_major_address(r, c, 3) for r in range(3) for c in range(5)}),
                         list(range(1000, 1015)))
        self.assertEqual(set(ex.walk_strides(3, 5)), {1})
        self.assertEqual(sorted(set(ex.walk_strides(3, 5, by_rows=False))), [-9, 5])
        self.assertEqual(ex.walk_strides(1, 1), [])


if __name__ == "__main__":
    unittest.main()
