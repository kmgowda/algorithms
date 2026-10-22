import random
import unittest

import ch17_examples as ex


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

    def test_lazy_trace(self) -> None:
        lz = ex.LazySegmentTree(ex.DAYS)
        self.assertEqual((lz.range_add(2, 5, 1), lz.visited), ([(2, 3), (4, 5)], 7))
        self.assertEqual((lz.tags(), lz.t[1], lz.t[2], lz.t[3]), ({(2, 3): 1, (4, 5): 1}, 35, 11, 24))
        self.assertEqual((lz.query(3, 4), lz.visited, lz.tags()), (8, 11, {}))
        self.assertEqual(lz.query(0, 7), 35)

    def test_lazy_every_case(self) -> None:
        lz = ex.LazySegmentTree(ex.DAYS)
        self.assertEqual((lz.range_add(0, 7, 2), lz.visited, lz.tags()), ([(0, 7)], 1, {(0, 7): 2}))
        self.assertEqual(lz.query(5, 5), 11)
        self.assertEqual((lz.range_add(5, 2, 9), lz.query(0, 7)), ([], 47))      # empty range: nothing changes
        one = ex.LazySegmentTree([7])
        one.range_add(0, 0, 3)
        self.assertEqual((one.query(0, 0), one.tags()), (10, {}))
        empty = ex.LazySegmentTree([])
        self.assertEqual((empty.range_add(0, 3, 1), empty.query(0, 3)), ([], 0))

    def test_lazy_against_plain_list(self) -> None:
        rng = random.Random(2)
        for n in (1, 2, 3, 7, 8, 13, 40):
            vals = [rng.randint(0, 9) for _ in range(n)]
            lz = ex.LazySegmentTree(vals)
            for _ in range(300):
                a = rng.randrange(n); b = rng.randrange(a, n)
                if rng.random() < 0.5:
                    d = rng.randint(-5, 5)
                    lz.range_add(a, b, d)
                    for i in range(a, b + 1):
                        vals[i] += d
                else:
                    self.assertEqual(lz.query(a, b), sum(vals[a:b + 1]))
                    self.assertLessEqual(lz.visited, 4 * max(1, n.bit_length()) + 1)

    def test_dashboard(self) -> None:
        steps = ex.dashboard_day()
        self.assertEqual(steps, {"prefix sums": 1016481, "plain array": 1262803, "segment tree": 180735})


if __name__ == "__main__":
    unittest.main()
