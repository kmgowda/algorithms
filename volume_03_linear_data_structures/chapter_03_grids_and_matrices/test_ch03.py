import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestGrids(unittest.TestCase):
    def test_make_grid_independent_rows(self) -> None:
        g = ex.make_grid(2, 3)
        g[0][0] = 9
        self.assertEqual(g, [[9, 0, 0], [0, 0, 0]])

    def test_flat_grid(self) -> None:
        g = ex.FlatGrid(2, 3, ".")
        g[1, 2] = "X"
        self.assertEqual(g[1, 2], "X")
        self.assertEqual(g.to_rows(), [[".", ".", "."], [".", ".", "X"]])
        with self.assertRaises(IndexError):
            g[2, 0]
        with self.assertRaises(ValueError):
            ex.FlatGrid(0, 3)

    def test_transforms(self) -> None:
        board = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(ex.transpose(board), [[1, 4], [2, 5], [3, 6]])
        self.assertEqual(ex.rotate_clockwise(board), [[4, 1], [5, 2], [6, 3]])
        square = [[1, 2], [3, 4]]
        r = square
        for _ in range(4):
            r = ex.rotate_clockwise(r)
        self.assertEqual(r, square)

    def test_spiral(self) -> None:
        self.assertEqual(ex.spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]),
                         [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7])
        self.assertEqual(ex.spiral_order([[1], [2], [3]]), [1, 2, 3])
        self.assertEqual(ex.spiral_order([[1, 2, 3]]), [1, 2, 3])
        self.assertEqual(ex.spiral_order([]), [])
        rng = random.Random(2)
        for _ in range(100):
            rows, cols = rng.randint(1, 6), rng.randint(1, 6)
            grid = [[r * cols + c for c in range(cols)] for r in range(rows)]
            self.assertEqual(sorted(ex.spiral_order(grid)), list(range(rows * cols)))

    def test_neighbors_seats_blur(self) -> None:
        board = ex.make_grid(3, 3)
        self.assertEqual(sorted(ex.neighbors(board, 0, 0)), [(0, 1), (1, 0)])
        self.assertEqual(len(list(ex.neighbors(board, 1, 1))), 4)
        cinema = [[1, 1, 1, 1, 1], [1, 1, 0, 1, 1], [0, 1, 1, 0, 1], [0, 0, 0, 0, 0]]
        self.assertEqual(ex.best_free_seat(cinema), (1, 2))   # ties with (2, 3); first found wins
        self.assertIsNone(ex.best_free_seat([[1, 1]]))
        self.assertEqual(ex.box_blur([[0, 0, 0], [0, 255, 0], [0, 0, 0]])[1][1], 51)

    def test_matrix_multiply(self) -> None:
        self.assertEqual(ex.matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]])
        identity = [[1, 0], [0, 1]]
        self.assertEqual(ex.matrix_multiply(identity, [[3], [4]]), [[3], [4]])
        with self.assertRaises(ValueError):
            ex.matrix_multiply([[1, 2]], [[1, 2]])


class TestSolutions(unittest.TestCase):
    def test_totals_and_mirror(self) -> None:
        self.assertEqual(sol.row_and_column_totals([[5, 3], [2, 7]]), ([8, 9], [7, 10]))
        self.assertEqual(sol.mirror_image([[1, 0, 0], [1, 1, 0]]), [[0, 0, 1], [0, 1, 1]])

    def test_set_zeroes(self) -> None:
        g = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
        sol.set_zeroes(g)
        self.assertEqual(g, [[1, 0, 1], [0, 0, 0], [1, 0, 1]])

    def test_sorted_matrix(self) -> None:
        grid = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
        for value in range(0, 20):
            self.assertEqual(sol.search_sorted_matrix(grid, value), any(value in row for row in grid))
        self.assertFalse(sol.search_sorted_matrix([], 1))

    def test_life_and_edges(self) -> None:
        blinker = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
        self.assertEqual(sol.life_step(blinker), [[0, 0, 0], [1, 1, 1], [0, 0, 0]])
        self.assertEqual(sol.life_step(sol.life_step(blinker)), blinker)
        self.assertEqual(sol.count_edge_cells([[0] * 4 for _ in range(3)]), 10)


if __name__ == "__main__":
    unittest.main()
