import sys
import unittest
from collections import Counter

import ch09_examples as ex


class TestChapter1(unittest.TestCase):
    def test_stairs(self) -> None:
        c = Counter()
        self.assertEqual((ex.ways(6, calls=c), sum(c.values()), c[0], c[1]), (13, 41, 13, 8))
        got = []
        for n in (10, 20, 30):
            c, s = Counter(), [0]
            got.append((ex.ways(n, calls=c), sum(c.values()), ex.ways_memo(n, solved=s), s[0]))
        self.assertEqual(got, [(89, 287, 89, 10), (10946, 35421, 10946, 20), (1346269, 4356617, 1346269, 30)])

    def test_every_case(self) -> None:
        self.assertEqual((ex.ways(10, (1, 2, 3)), ex.ways_memo(50)), (274, 20365011074))
        self.assertEqual((ex.ways_memo(10, (2,)), ex.ways_memo(9, (2,)), ex.ways(0), ex.ways_memo(0)), (1, 0, 1, 1))
        self.assertEqual([ex.ways_memo(n, (3, 5)) for n in (10, 7, 4)], [1, 0, 0])
        self.assertEqual(([ex.ways_memo(n, (1, 2, 3)) for n in range(7)], ex.ways_memo(7)), ([1, 1, 2, 4, 7, 13, 24], 21))
        old = sys.getrecursionlimit()
        sys.setrecursionlimit(10000)
        try:
            with self.assertRaises(RecursionError):
                ex.ways_memo(5000)
        finally:
            sys.setrecursionlimit(old)


class TestCallCounting(unittest.TestCase):
    def test_plain_calls(self) -> None:
        self.assertEqual([ex.plain_calls(n) for n in (5, 6, 10, 20, 30)], [25, 41, 287, 35421, 4356617])
        self.assertEqual(ex.plain_calls(30, (1, 2, 3)), 192299281)
        self.assertEqual((ex.plain_calls(0), ex.plain_calls(-1), ex.plain_calls(1)), (1, 1, 3))
        c = Counter()
        ex.ways(12, (1, 2, 3), calls=c)
        self.assertEqual(sum(c.values()), ex.plain_calls(12, (1, 2, 3)))

    def test_book_numbers(self) -> None:
        self.assertEqual(ex.ways_memo(30, (1, 2, 3)), 53798080)
        self.assertTrue(all(ex.plain_calls(n) == 2 * ex.ways_memo(n + 1) - 1 for n in range(25)))
        self.assertEqual((ex.ways_avoiding(6, {3}), ex.ways_avoiding(6), ex.ways_avoiding(0, {0})), (4, 13, 0))

    def test_memo_trace(self) -> None:
        t = ex.memo_trace(5)
        self.assertEqual([m for e, m in t if e == "solve"], [5, 4, 3, 2, 1])
        self.assertEqual([m for e, m in t if e == "look up"], [1, 2, 3])
        self.assertEqual((ex.memo_trace(0), ex.memo_trace(1)), ([], [("solve", 1)]))


if __name__ == "__main__":
    unittest.main()
