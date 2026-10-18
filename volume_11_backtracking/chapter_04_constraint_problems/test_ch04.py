import itertools
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


class TestConstraintProblems(unittest.TestCase):
    def test_queens(self) -> None:
        known = [1, 0, 0, 2, 10, 4, 40, 92, 352]
        for n in range(1, 10):
            sols = ex.n_queens(n)
            self.assertEqual(len(sols), known[n - 1])
            self.assertEqual(sol.count_queens_bits(n), known[n - 1])
            self.assertTrue(all(sol.queens_are_safe(s) for s in sols))
        for n in range(1, 7):
            brute = [list(p) for p in itertools.permutations(range(n)) if sol.queens_are_safe(list(p))]
            self.assertEqual(ex.n_queens(n), brute)

    def test_sudoku(self) -> None:
        board = [row[:] for row in ex.PUZZLE]
        self.assertTrue(ex.solve_sudoku(board))
        self.assertTrue(ex.is_valid_sudoku(board))
        self.assertTrue(all(board[r][c] == ex.PUZZLE[r][c] for r in range(9) for c in range(9) if ex.PUZZLE[r][c]))
        bad = [row[:] for row in ex.PUZZLE]
        bad[0][2] = 5                                     # two 5s in the first row: impossible
        self.assertFalse(ex.solve_sudoku(bad))

    def test_words(self) -> None:
        rng = random.Random(1)
        grid = ["ABCE", "SFCS", "ADEE"]
        self.assertTrue(ex.word_search(grid, "ABCCED"))
        self.assertTrue(ex.word_search(grid, "SEE"))
        self.assertFalse(ex.word_search(grid, "ABCB"))
        self.assertEqual(sol.find_all_words(["oaan", "etae", "ihkr", "iflv"], ["oath", "pea", "eat", "rain"]), ["eat", "oath"])
        for _ in range(30):
            g = ["".join(rng.choice("ab") for _ in range(3)) for _ in range(3)]
            words = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 5))) for _ in range(5)]
            self.assertEqual(sol.find_all_words(g, words), sorted({w for w in words if ex.word_search(g, w)}))

    def test_seating(self) -> None:
        plan = ex.exam_seating(["A1", "A2", "B1", "B2"], {frozenset({"A1", "A2"}), frozenset({"B1", "B2"})}, 4)
        self.assertEqual(len(plan), 4)
        self.assertIsNone(ex.exam_seating(["A1", "A2"], {frozenset({"A1", "A2"})}, 2))


if __name__ == "__main__":
    unittest.main()
