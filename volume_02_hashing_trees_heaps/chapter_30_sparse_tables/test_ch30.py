import random
import unittest

import ch30_examples as ex


class TestChapter59(unittest.TestCase):
    def test_every_case(self) -> None:
        s = ex.SparseTable([3, 1, 4, 1, 5, 9, 2, 6])
        self.assertEqual(s.query(0, 7), (1, (0, 7), (0, 7)))
        self.assertEqual(s.query(2, 5)[0], 1)
        self.assertEqual(s.query(4, 6), (2, (4, 5), (5, 6)))
        self.assertEqual((s.query(0, 0)[0], s.query(7, 7)[0]), (3, 6))
        self.assertEqual(ex.SparseTable([2, 2, 2]).query(0, 2), (2, (0, 1), (1, 2)))
        for a, b in ((5, 2), (0, 20), (-1, 3)):
            with self.assertRaises(IndexError):
                s.query(a, b)
        self.assertEqual((s.cells(), ex.SparseTable([]).cells(), ex.SparseTable([7]).query(0, 0)[0]), (21, 0, 7))

    def test_against_scans(self) -> None:
        rng = random.Random(1)
        for n in (1, 2, 7, 8, 33, 100):
            vals = [rng.randint(0, 50) for _ in range(n)]
            st = ex.SparseTable(vals)
            for _ in range(200):
                a = rng.randrange(n); b = rng.randrange(a, n)
                self.assertEqual(st.query(a, b)[0], min(vals[a:b + 1]))

    def test_examples(self) -> None:
        st = ex.SparseTable(ex.NOISE)
        self.assertEqual(st.table[1:], [[3, 3, 4, 4, 2, 2, 8], [3, 3, 2, 2, 2], [2]])
        self.assertEqual(st.query(1, 6), (2, (1, 4), (3, 6)))
        self.assertEqual(st.query(2, 4), (4, (2, 3), (3, 4)))
        self.assertEqual(len(ex.SparseTable(list(range(100))).table), 7)


if __name__ == "__main__":
    unittest.main()
