import unittest

import ch28_examples as ex


class TestChapter28(unittest.TestCase):
    def test_queens(self) -> None:
        got = [(len(s), n) for s, n in (ex.queens(k) for k in (1, 2, 3, 4, 5, 6, 8))]
        self.assertEqual(got, [(1, 2), (0, 3), (0, 6), (2, 17), (10, 54), (4, 153), (92, 2057)])
        self.assertEqual(ex.queens(8, True), ([[0, 4, 7, 5, 2, 6, 1, 3]], 114))

    def test_every_case(self) -> None:
        self.assertEqual(ex.sudoku(ex.PUZZLE4), ([[1, 3, 2, 4], [4, 2, 3, 1], [2, 4, 1, 3], [3, 1, 4, 2]], 15))
        self.assertEqual(ex.sudoku([[1, 1, 0, 0], [0] * 4, [0] * 4, [0] * 4]), (None, 0))
        self.assertEqual(ex.sudoku([[0] * 4 for _ in range(4)])[1], 16)


if __name__ == "__main__":
    unittest.main()
