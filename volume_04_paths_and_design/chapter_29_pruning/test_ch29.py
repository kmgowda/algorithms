import random
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


    def test_exact_cover(self) -> None:
        log = []
        self.assertEqual(ex.algorithm_x(ex.DUTIES, ex.TEAMS, log), ([["A", "B", "F"]], 5))
        self.assertEqual(log, [("Storytime", 2), ("Tea", 1), ("Displays", 1), ("Desk", 0)])
        self.assertEqual(ex.exact_cover_brute(ex.DUTIES, ex.TEAMS), [["A", "B", "F"]])
        more = dict(ex.TEAMS, H=["Displays", "Leaflets"])
        self.assertEqual(ex.algorithm_x(ex.DUTIES, more), ([["A", "B", "F"], ["A", "B", "H"]], 6))
        self.assertEqual((ex.algorithm_x([], {}), ex.algorithm_x(["X"], {})), (([[]], 1), ([], 1)))
        rng = random.Random(29)
        for _ in range(300):
            cols = list("abcdef")[:rng.randint(1, 6)]
            rows = {i: rng.sample(cols, rng.randint(1, len(cols))) for i in range(rng.randint(0, 8))}
            self.assertEqual(sorted(ex.algorithm_x(cols, rows)[0]), sorted(ex.exact_cover_brute(cols, rows)))

    def test_links_restore(self) -> None:
        head = ex.build_links(ex.DUTIES, ex.TEAMS)
        sizes = lambda: [(c.name, c.size) for c in self._ring(head)]  # noqa: E731
        before = sizes()
        col = head.right.right.right                   # Storytime
        ex.cover(col)
        self.assertEqual([n for n, _ in sizes()], ["Desk", "Shelving", "Displays", "Tea", "Leaflets"])
        self.assertEqual(dict(sizes())["Displays"], 2)    # D, which needs Storytime, has left the Displays column
        ex.uncover(col)
        self.assertEqual(sizes(), before)

    @staticmethod
    def _ring(head):
        c = head.right
        while c is not head:
            yield c
            c = c.right

    def test_sudoku_as_cover(self) -> None:
        p4 = [[1, 0, 0, 0], [0, 0, 3, 0], [0, 4, 0, 0], [0, 0, 0, 2]]
        self.assertEqual(ex.sudoku_exact_cover(p4), ([[1, 3, 2, 4], [4, 2, 3, 1], [2, 4, 1, 3], [3, 1, 4, 2]], 17))
        solved, nodes = ex.sudoku_exact_cover(ex.GRID)
        self.assertEqual((solved, nodes), (ex.sudoku(ex.GRID, True)[0], 82))
        self.assertEqual(ex.sudoku_exact_cover([[1, 1, 0, 0], [0] * 4, [0] * 4, [0] * 4])[0], None)


if __name__ == "__main__":
    unittest.main()
