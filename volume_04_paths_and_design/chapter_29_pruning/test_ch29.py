import unittest

import ch29_examples as ex


class TestChapter29(unittest.TestCase):
    def test_vouchers(self) -> None:
        got = [ex.subset_sum(ex.VOUCHERS, ex.TARGET, p, s) for p in (False, True) for s in (False, True)]
        self.assertEqual([n for _, n in got], [245, 884, 39, 14])
        self.assertTrue(all(sum(v) == 50 for v, _ in got))
        self.assertEqual((ex.sudoku(ex.GRID, False)[1], ex.sudoku(ex.GRID, True)[1]), (4208, 51))
        self.assertEqual(ex.sudoku(ex.GRID, True)[0], ex.sudoku(ex.GRID, False)[0])

    def test_every_case(self) -> None:
        self.assertEqual(ex.subset_sum(ex.VOUCHERS, 200, True, True), (None, 1))
        self.assertEqual(ex.subset_sum(ex.VOUCHERS, 200, False, False)[1], 2047)
        self.assertEqual((ex.subset_sum([], 0, True, True), ex.subset_sum([], 5, True, True)), (([], 1), (None, 1)))
        self.assertEqual(ex.subset_sum(ex.VOUCHERS, 1, True, True), (None, 21))
        self.assertEqual(ex.subset_sum(ex.VOUCHERS, 10, True, True)[0], [8, 2])


if __name__ == "__main__":
    unittest.main()
