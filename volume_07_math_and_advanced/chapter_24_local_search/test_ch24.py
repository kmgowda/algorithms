import random
import unittest

import ch24_examples as ex


class TestChapter24(unittest.TestCase):
    def test_examples(self) -> None:
        pts = ex.places(12, 1)
        start = list(range(12))
        t2, moves = ex.two_opt(start, pts)
        ta = ex.annealing(start, pts, random.Random(24))
        self.assertEqual((round(ex.length(start, pts), 1), round(ex.length(t2, pts), 1), moves, round(ex.length(ta, pts), 1), round(ex.exact(pts), 1)),
                         (687.8, 397.4, 11, 391.9, 391.9))
        stuck = [round(ex.length(ex.two_opt(random.Random(s).sample(range(12), 12), pts)[0], pts), 1) for s in range(10)]
        self.assertEqual(stuck.count(391.9), 3)

    def test_every_case(self) -> None:
        pts = ex.places(12, 1)
        self.assertEqual((ex.length([0], pts), ex.two_opt([0, 1], pts), ex.two_opt([0, 1, 2], pts)[1]), (0.0, ([0, 1], 0), 0))
        for s in range(5):
            t = random.Random(s).sample(range(8), 8)
            self.assertEqual(sorted(ex.two_opt(t, pts[:8])[0]), list(range(8)))
            self.assertGreaterEqual(round(ex.length(ex.two_opt(t, pts[:8])[0], pts), 6), round(ex.exact(pts[:8]), 6))


class TestDepth(unittest.TestCase):
    def test_delta_and_restarts(self) -> None:
        pts = ex.places(12, 1)
        r = random.Random(30)
        for _ in range(200):
            tour = r.sample(range(12), 12)
            i, j = sorted(r.sample(range(1, 12), 2))
            new = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
            self.assertAlmostEqual(ex.two_opt_delta(tour, pts, i, j), ex.length(new, pts) - ex.length(tour, pts))
        self.assertEqual(ex.restarts(pts, 20, 100), (391.9, 9))

    def test_max_cut_and_colouring(self) -> None:
        side, cut, moves = ex.max_cut_local(ex.TOWN, ex.ROADS)
        self.assertEqual((cut, moves, ex.max_cut_brute(ex.TOWN, ex.ROADS)), (10, 6, 10))
        r = random.Random(31)
        import itertools
        for _ in range(200):
            vs = list(range(r.randint(2, 8)))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.5]
            start = {v: r.randrange(2) for v in vs}
            _, c, _ = ex.max_cut_local(vs, es, start)
            self.assertGreaterEqual(2 * c, len(es))
            self.assertLessEqual(c, ex.max_cut_brute(vs, es))
        col, steps = ex.min_conflicts_colouring(ex.TOWN, ex.ROADS, 3, random.Random(5))
        self.assertEqual(steps, 8)
        self.assertTrue(all(col[a] != col[b] for a, b in ex.ROADS))
        self.assertEqual(ex.min_conflicts_colouring(ex.TOWN, ex.ROADS, 2, random.Random(5), steps=200), (None, 200))


if __name__ == "__main__":
    unittest.main()
