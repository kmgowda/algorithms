import random
import unittest

import ch28_examples as ex


class TestChapter57(unittest.TestCase):
    def test_every_case(self) -> None:
        v = [3, 1, 4, 1, 5, 9, 2, 6]
        s = ex.SegmentTree(v)
        self.assertEqual((s.query(0, 7), s.visited), (31, 1))
        self.assertEqual([s.query(i, i) for i in (3, 0, 7)], [1, 3, 6])
        self.assertEqual(s.query(2, 5), 19)
        self.assertEqual((s.query(1, 6), s.visited, s.used_nodes(1, 6)), (22, 11, [(1, 1), (2, 3), (4, 5), (6, 6)]))
        self.assertEqual((s.query(5, 2), s.query(0, 20)), (0, 31))
        self.assertEqual(s.update(3, 10), [1, 2, 5, 11])
        self.assertEqual(s.query(0, 7), 40)
        self.assertEqual([ex.SegmentTree(v).update(i, 0) for i in (0, 7)], [[1, 2, 4, 8], [1, 3, 7, 15]])
        self.assertEqual(ex.SegmentTree([7]).query(0, 0), 7)
        self.assertEqual(ex.SegmentTree([]).query(0, 0), 0)

    def test_against_plain_sums(self) -> None:
        rng = random.Random(1)
        for n in (1, 2, 5, 8, 13, 40):
            vals = [rng.randint(0, 9) for _ in range(n)]
            st = ex.SegmentTree(vals)
            for _ in range(200):
                if rng.random() < 0.4:
                    i, v = rng.randrange(n), rng.randint(0, 9)
                    st.update(i, v)
                    vals[i] = v
                a = rng.randrange(n); b = rng.randrange(a, n)
                self.assertEqual(st.query(a, b), sum(vals[a:b + 1]))

    def test_examples(self) -> None:
        st = ex.SegmentTree(ex.DAYS)
        self.assertEqual(st.t[1:16], [31, 9, 22, 4, 5, 14, 8, 3, 1, 4, 1, 5, 9, 2, 6])
        self.assertEqual(st.query(1, 6), 22)
        self.assertEqual(st.used_nodes(1, 6), [(1, 1), (2, 3), (4, 5), (6, 6)])
        self.assertEqual(st.used_nodes(0, 5), [(0, 3), (4, 5)])
        st.update(5, 4)
        self.assertEqual((st.t[1], st.query(1, 6)), (26, 17))


if __name__ == "__main__":
    unittest.main()
