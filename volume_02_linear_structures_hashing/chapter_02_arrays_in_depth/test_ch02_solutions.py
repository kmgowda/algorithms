import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_most_all_lonely_is_half_rounded_up(self) -> None:
        for rows, cols in ((1, 1), (1, 2), (1, 5), (2, 2), (2, 3), (3, 3), (3, 4)):
            self.assertEqual(sol.most_all_lonely(rows, cols), (rows * cols + 1) // 2)

    def test_chessboard_seating_is_all_lonely(self) -> None:
        grid = [[1 if (r + c) % 2 == 0 else 0 for c in range(5)] for r in range(3)]
        self.assertEqual(len(ex.lonely_seats(grid)), 8)

    def test_rotate_smallest(self) -> None:
        empty: list[list[int]] = []
        sol.rotate_clockwise(empty)
        self.assertEqual(empty, [])
        one = [[7]]
        sol.rotate_clockwise(one)
        self.assertEqual(one, [[7]])

    def test_rotate_example(self) -> None:
        g = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        sol.rotate_clockwise(g)
        self.assertEqual(g, [[7, 4, 1], [8, 5, 2], [9, 6, 3]])

    def test_rotate_matches_formula(self) -> None:
        rng = random.Random(2)
        for n in range(2, 8):
            g = [[rng.randint(0, 9) for _ in range(n)] for _ in range(n)]
            want = [[g[n - 1 - c][r] for c in range(n)] for r in range(n)]
            sol.rotate_clockwise(g)
            self.assertEqual(g, want)

    def test_half_checked_edge_is_wrong(self) -> None:
        self.assertEqual(sol.lonely_seats_no_lower_check(ex.SEATS), [(0, 1), (1, 0), (2, 4)])
        self.assertIn((0, 4), ex.lonely_seats(ex.SEATS))

    def test_row_append_copies(self) -> None:
        self.assertEqual([ex.row_append_copies(n) for n in (0, 1, 2, 5, 1000)], [0, 0, 1, 7, 1023])
        for n in range(1, 300):
            self.assertLess(ex.row_append_copies(n), 2 * n)


if __name__ == "__main__":
    unittest.main()
