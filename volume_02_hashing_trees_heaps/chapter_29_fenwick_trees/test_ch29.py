import random
import unittest

import ch29_examples as ex


class TestChapter58(unittest.TestCase):
    def test_every_case(self) -> None:
        v = [3, 1, 4, 1, 5, 9, 2, 6]
        f = ex.Fenwick(v)
        self.assertEqual((f.prefix(0), f.prefix(8), f.prefix(7)), ((0, []), (31, [8]), (25, [7, 6, 4])))
        self.assertEqual((f.range_sum(4, 4), f.range_sum(1, 8), f.range_sum(5, 2)), (1, 31, -5))
        self.assertEqual([ex.Fenwick(v).add(i, 0) for i in (1, 8, 5, 9)], [[1, 2, 4, 8], [8], [5, 6, 8], []])
        with self.assertRaises(IndexError):
            ex.Fenwick(v).add(0, 5)
        self.assertEqual((ex.Fenwick([]).prefix(0)[0], ex.Fenwick([7]).prefix(1)[0]), (0, 7))

    def test_against_plain_sums(self) -> None:
        rng = random.Random(1)
        for n in (1, 5, 8, 13, 50):
            vals = [rng.randint(0, 9) for _ in range(n)]
            f = ex.Fenwick(vals)
            for _ in range(200):
                if rng.random() < 0.4:
                    i, d = rng.randint(1, n), rng.randint(-3, 3)
                    f.add(i, d)
                    vals[i - 1] += d
                a = rng.randint(1, n); b = rng.randint(a, n)
                self.assertEqual(f.range_sum(a, b), sum(vals[a - 1:b]))

    def test_examples(self) -> None:
        f = ex.Fenwick(ex.DAYS)
        self.assertEqual(f.tree[1:], [3, 4, 4, 9, 5, 14, 2, 31])
        self.assertEqual(f.prefix(7), (25, [7, 6, 4]))
        self.assertEqual(f.prefix(6), (23, [6, 4]))
        self.assertEqual(f.range_sum(3, 6), 19)
        self.assertEqual(f.add(6, -5), [6, 8])
        self.assertEqual(f.range_sum(2, 7), 17)
        self.assertEqual(ex.Fenwick([0] * 8).add(3, 2), [3, 4, 8])
        self.assertEqual([ex.lowbit(i) for i in (12, 20, 7)], [4, 4, 1])
        self.assertEqual(ex.ranks([72, 95, 41, 88, 60]), [0, 1, 0, 2, 1])
        self.assertEqual(ex.ranks([50, 20, 70, 30]), [0, 0, 2, 1])

    def test_build_linear(self) -> None:
        f, moves = ex.build_linear(ex.DAYS)
        self.assertEqual((f.tree[1:], moves), ([3, 4, 4, 9, 5, 14, 2, 31],
                                               [(1, 2), (2, 4), (3, 4), (4, 8), (5, 6), (6, 8), (7, 8)]))
        rng = random.Random(3)
        for n in (0, 1, 2, 7, 16, 33):
            vals = [rng.randint(-9, 9) for _ in range(n)]
            self.assertEqual(ex.build_linear(vals)[0].tree, ex.Fenwick(vals).tree)

    def test_range_fenwick(self) -> None:
        r = ex.RangeFenwick(8)
        r.range_add(2, 5, 3)
        r.range_add(4, 8, 2)
        self.assertEqual([r.range_sum(i, i) for i in range(1, 9)], [0, 3, 3, 5, 5, 2, 2, 2])
        self.assertEqual((r.range_sum(1, 8), r.range_sum(3, 6)), (22, 15))
        one = ex.RangeFenwick(1)
        one.range_add(1, 1, 4)
        one.range_add(1, 0, 9)                        # an empty range changes nothing
        self.assertEqual(one.range_sum(1, 1), 4)
        rng = random.Random(4)
        for n in (1, 2, 5, 8, 13, 40):
            r, vals = ex.RangeFenwick(n), [0] * n
            for _ in range(300):
                a = rng.randint(1, n); b = rng.randint(a, n)
                if rng.random() < 0.5:
                    d = rng.randint(-5, 5)
                    r.range_add(a, b, d)
                    for i in range(a - 1, b):
                        vals[i] += d
                else:
                    self.assertEqual(r.range_sum(a, b), sum(vals[a - 1:b]))


if __name__ == "__main__":
    unittest.main()
