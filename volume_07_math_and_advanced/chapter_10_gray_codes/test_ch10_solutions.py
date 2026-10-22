import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_one_bit_at_lowest_set_bit(self) -> None:
        for k in range(1, 1 << 14):
            self.assertEqual(ex.gray(k - 1) ^ ex.gray(k), k & -k)

    def test_subset_totals(self) -> None:
        w = [3, 5, 9]
        got = sol.subset_totals_gray(w)
        self.assertEqual(got, [(0, 0), (1, 3), (3, 8), (2, 5), (6, 14), (7, 17), (5, 12), (4, 9)])
        self.assertEqual(sol.subset_totals_gray([]), [(0, 0)])
        for mask, total in sol.subset_totals_gray([2, 7, 1, 8, 2, 8]):
            self.assertEqual(total, sum(x for i, x in enumerate([2, 7, 1, 8, 2, 8]) if mask >> i & 1))
        self.assertEqual(len({m for m, _ in sol.subset_totals_gray([1] * 8)}), 256)

    def test_wrong_decode(self) -> None:
        self.assertEqual(sol.first_wrong_decode(), 4)
        self.assertEqual((sol.wrong_from_gray(4), ex.from_gray(4)), (6, 7))
        for g in range(4):
            self.assertEqual(sol.wrong_from_gray(g), ex.from_gray(g))


if __name__ == "__main__":
    unittest.main()
