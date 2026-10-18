import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


def rand_grid(rng, rows, cols, lo=-5, hi=9):
    return [[rng.randint(lo, hi) for _ in range(cols)] for _ in range(rows)]


class TestMatrix(unittest.TestCase):
    def test_rectangle_totals(self) -> None:
        rng = random.Random(1)
        for _ in range(100):
            rows, cols = rng.randint(1, 6), rng.randint(1, 6)
            g = rand_grid(rng, rows, cols)
            rt = ex.RectangleTotals(g)
            r1, r2 = sorted(rng.randrange(rows) for _ in range(2))
            c1, c2 = sorted(rng.randrange(cols) for _ in range(2))
            self.assertEqual(rt.total(r1, c1, r2, c2), sum(g[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)))

    def test_densest(self) -> None:
        field = [[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1], [4, 1, 0, 5]]
        self.assertEqual(ex.densest_square(field, 2), (0, 0, 14))

    def test_toeplitz_and_zigzag(self) -> None:
        self.assertTrue(ex.is_toeplitz([[1, 2, 3], [4, 1, 2], [5, 4, 1]]))
        self.assertFalse(ex.is_toeplitz([[1, 2], [2, 2]]))
        self.assertEqual(ex.zigzag_diagonals([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), [1, 2, 4, 7, 5, 3, 6, 8, 9])
        self.assertEqual(ex.zigzag_diagonals([[1, 2], [3, 4], [5, 6]]), [1, 2, 3, 5, 4, 6])
        self.assertEqual(ex.zigzag_diagonals([]), [])

    def test_rotate(self) -> None:
        rng = random.Random(2)
        for n in range(1, 7):
            g = rand_grid(rng, n, n)
            expected = [list(row) for row in zip(*g[::-1])]
            ex.rotate_in_place(g)
            self.assertEqual(g, expected)

    def test_search(self) -> None:
        g = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
        for v in range(0, 62):
            self.assertEqual(ex.search_row_sorted(g, v), any(v in row for row in g))
        self.assertFalse(ex.search_row_sorted([], 1))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.block_sums([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1), [[12, 21, 16], [27, 45, 33], [24, 39, 28]])
        self.assertEqual(sol.anti_diagonal_groups([[1, 2], [3, 4]]), {0: [1], 1: [2, 3], 2: [4]})
        g = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        sol.transpose_in_place(g)
        self.assertEqual(g, [[1, 4, 7], [2, 5, 8], [3, 6, 9]])
        self.assertEqual(sol.count_bright_squares([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2, 16), 3)


if __name__ == "__main__":
    unittest.main()
