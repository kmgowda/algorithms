import itertools
import random
import unittest

import ch12_examples as ex


class TestChapter4(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(ex.fewest_coins(6, ex.ODD), (2, [3, 3], [0, 1, 2, 1, 1, 2, 2]))
        self.assertEqual(ex.fewest_coins(30, [25, 10, 1])[:2], (3, [10, 10, 10]))
        self.assertEqual(ex.best_evenings(ex.TALKS), (23, [1, 3, 6], [0, 6, 6, 15, 15, 18, 23, 23]))

    def test_every_case(self) -> None:
        self.assertEqual([ex.fewest_coins(a, c)[:2] for a, c in ((0, ex.ODD), (7, [5, 2]), (3, [5, 2]), (5, []))],
                         [(0, []), (2, [5, 2]), (None, []), (None, [])])
        self.assertEqual([ex.best_evenings(t)[:2] for t in ([], [5], [5, 9], [4, 4, 4, 4])],
                         [(0, []), (5, [1]), (9, [2]), (8, [1, 3])])
        self.assertEqual((ex.fewest_coins(8, ex.ODD)[0], ex.fewest_coins(14, [1, 7, 10, 22])[1], ex.best_evenings(ex.TALKS + [5])[0]), (2, [7, 7], 28))
        t = list(ex.TALKS)
        t[3] = 20
        self.assertEqual(ex.best_evenings(t)[:2], (34, [1, 4, 6]))
        self.assertEqual(max(a for a in range(40) if ex.fewest_coins(a, [4, 7])[0] is None), 17)
        for n in range(1, 9):
            talks = [(i * 7) % 10 + 1 for i in range(n)]
            brute = max(sum(talks[i] for i in s) for k in range(n + 1) for s in itertools.combinations(range(n), k)
                        if all(b - a > 1 for a, b in zip(s, s[1:])))
            self.assertEqual(ex.best_evenings(talks)[0], brute)


    def test_weighted_intervals(self) -> None:
        import random
        best, chosen, p, opt = ex.weighted_intervals(ex.BOOKINGS)
        self.assertEqual((best, chosen), (22, ["Story time", "Poetry", "Film club", "Book swap"]))
        self.assertEqual((p, opt), ([0, 1, 0, 3, 2, 4, 5], [0, 5, 8, 9, 13, 16, 20, 22]))
        self.assertEqual(ex.greedy_intervals(ex.BOOKINGS, key=lambda b: b[2])[0], 19)
        self.assertEqual(ex.greedy_intervals(ex.BOOKINGS, key=lambda b: -b[3])[0], 20)
        self.assertEqual(ex.weighted_intervals([])[:2], (0, []))
        self.assertEqual(ex.weighted_intervals([("A", 1, 2, 4)])[:2], (4, ["A"]))
        self.assertEqual(ex.weighted_intervals([("A", 1, 3, 4), ("B", 3, 5, 4)])[:2], (8, ["A", "B"]))
        big = [(a, b, c, 20 if a == "Chess club" else d) for a, b, c, d in ex.BOOKINGS]
        self.assertEqual(ex.weighted_intervals(big)[:2], (31, ["Chess club", "Knitting", "History talk"]))
        r = random.Random(4)
        for _ in range(200):
            bs = []
            for i in range(r.randint(0, 7)):
                s0 = r.randint(0, 10)
                bs.append((str(i), s0, s0 + r.randint(1, 4), r.randint(1, 9)))
            brute = max(sum(x[3] for x in c) for k in range(len(bs) + 1) for c in itertools.combinations(bs, k)
                        if all(a[2] <= b[1] or b[2] <= a[1] for a, b in itertools.combinations(c, 2)))
            got, names, _, _ = ex.weighted_intervals(bs)
            self.assertEqual(got, brute)
            self.assertEqual(sum(b[3] for b in bs if b[0] in names), got)


    def test_shelf_hull(self) -> None:
        best, cut = ex.shelf_hull(ex.WIDTHS, ex.BRACKET)
        self.assertEqual(best, [0, 29, 36, 72, 81, 126, 227, 251])
        self.assertEqual(ex.sections(ex.WIDTHS, cut), [[3, 1], [4, 1], [5], [9], [2]])
        self.assertEqual(ex.shelf_plain(ex.WIDTHS, ex.BRACKET)[2], 28)
        self.assertEqual(ex.shelf_hull([], 5), ([0], [0]))
        self.assertEqual(ex.shelf_hull([4], 5)[0], [0, 21])
        self.assertEqual(ex.shelf_hull([4], 20)[0][-1], 36)
        self.assertEqual(ex.shelf_hull([1, 1], 20)[0][-1], 24)
        self.assertEqual(ex.shelf_hull([1] * 6, 0)[0][-1], 6)       # free brackets: one book per section
        self.assertEqual(ex.sections([1] * 4, ex.shelf_hull([1] * 4, 100)[1]), [[1, 1, 1, 1]])
        r = random.Random(12)
        for _ in range(500):
            ws = [r.randint(1, 9) for _ in range(r.randint(0, 14))]
            c = r.randint(0, 80)
            best, cut = ex.shelf_hull(ws, c)
            self.assertEqual(best, ex.shelf_plain(ws, c)[0])
            parts = ex.sections(ws, cut)
            self.assertEqual(sum(sum(p) ** 2 + c for p in parts), best[-1])


if __name__ == "__main__":
    unittest.main()
