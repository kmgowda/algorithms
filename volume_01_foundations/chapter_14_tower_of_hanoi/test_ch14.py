import unittest

import ch14_examples as ex


class TestChapter14(unittest.TestCase):
    def test_every_case(self) -> None:
        for n, count, first in [(0, 0, None), (1, 1, ("A", "C")), (2, 3, ("A", "B")), (3, 7, ("A", "C")),
                                (4, 15, ("A", "B")), (5, 31, ("A", "C"))]:
            moves = []
            ex.hanoi(n, "A", "C", "B", moves)
            self.assertEqual(len(moves), count)
            self.assertEqual(moves[0] if moves else None, first)
            self.assertEqual(ex.replay(n, moves)["C"], list(range(n, 0, -1)))
        with self.assertRaises(AssertionError):
            ex.replay(2, [("A", "C"), ("A", "C")])
        with self.assertRaises(AssertionError):
            ex.replay(1, [("B", "C")])

    def test_solutions(self) -> None:
        for n in range(0, 12):
            moves = []
            ex.hanoi(n, "A", "C", "B", moves)
            self.assertEqual(len(moves), 2 ** n - 1)
            self.assertEqual(ex.move_count(n), 2 ** n - 1)
            self.assertEqual(ex.replay(n, moves), {"A": [], "B": [], "C": list(range(n, 0, -1))})
        three = []
        ex.hanoi(3, "A", "C", "B", three)
        self.assertEqual(three, [("A", "C"), ("A", "B"), ("C", "B"), ("A", "C"), ("B", "A"), ("B", "C"), ("A", "C")])
        four = []
        ex.hanoi(4, "A", "C", "B", four)
        self.assertEqual(" ".join(a + b for a, b in four), "AB AC BC AB CA CB AB AC BC BA CA BC AB AC BC")

    def test_hanoi_with_stack(self) -> None:
        self.assertEqual(ex.hanoi_with_stack(0, "A", "C", "B"), [])
        self.assertEqual(ex.hanoi_with_stack(1, "A", "C", "B"), [("A", "C")])
        for n in range(0, 11):
            rec: list[tuple[str, str]] = []
            ex.hanoi(n, "A", "C", "B", rec)
            self.assertEqual(ex.hanoi_with_stack(n, "A", "C", "B"), rec)
        snaps: list[list[str]] = []
        ex.hanoi_with_stack(3, "A", "C", "B", snaps)
        self.assertEqual(max(len(t) for t in snaps), 5)                # 2n - 1 tasks at most for n = 3
        self.assertEqual(snaps[-1], [])
        for n in range(1, 9):
            snaps = []
            ex.hanoi_with_stack(n, "A", "C", "B", snaps)
            self.assertEqual(max(len(t) for t in snaps), 2 * n - 1)

    def test_disk_counts_and_adjacent(self) -> None:
        self.assertEqual(ex.moves_of_each_disk(4), [8, 4, 2, 1])
        self.assertEqual(ex.moves_of_each_disk(0), [])
        for n in range(1, 9):
            self.assertEqual(ex.moves_of_each_disk(n), [2 ** (n - k) for k in range(1, n + 1)])
        for n in range(0, 7):
            adj: list[tuple[str, str]] = []
            ex.adjacent_hanoi(n, "A", "C", "B", adj)
            self.assertEqual(len(adj), 3 ** n - 1)
            self.assertTrue(all({a, b} != {"A", "C"} for a, b in adj))   # never jumps between the ends
            self.assertEqual(ex.replay(n, adj), {"A": [], "B": [], "C": list(range(n, 0, -1))})


if __name__ == "__main__":
    unittest.main()
