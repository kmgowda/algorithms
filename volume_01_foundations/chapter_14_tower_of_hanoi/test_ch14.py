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


if __name__ == "__main__":
    unittest.main()
