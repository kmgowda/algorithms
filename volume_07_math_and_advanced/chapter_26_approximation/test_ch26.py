import itertools
import random
import unittest

import ch26_examples as ex


class TestChapter26(unittest.TestCase):
    def test_examples(self) -> None:
        c = ex.cover_by_matching(ex.ROADS)
        self.assertEqual((len(c), len(ex.smallest_cover(ex.TOWN, ex.ROADS))), (8, 4))
        boxes = [7, 6, 5, 4, 4, 3, 2, 2, 2, 1]
        self.assertEqual((ex.first_fit_decreasing(boxes, 10), ex.fewest_bins(boxes, 10)), ([[7, 3], [6, 4], [5, 4, 1], [2, 2, 2]], 4))

    def test_every_case(self) -> None:
        self.assertEqual((ex.cover_by_matching([]), ex.first_fit_decreasing([], 10), ex.first_fit_decreasing([10, 10], 10), ex.cover_by_matching([("a", "b")])),
                         ([], [], [[10], [10]], ["a", "b"]))
        with self.assertRaises(ValueError):
            ex.first_fit_decreasing([11], 10)
        roads = [("Market", "Station")] + [x for x in ex.ROADS if x != ("Market", "Station")]
        self.assertEqual((len(ex.cover_by_matching(roads)), ex.first_fit_decreasing([6, 5, 5, 4], 10)), (8, [[6, 4], [5, 5]]))
        tri = [("a", "b"), ("b", "c"), ("a", "c")]
        self.assertEqual((len(ex.cover_by_matching(tri)), len(ex.smallest_cover(["a", "b", "c"], tri))), (2, 2))
        r = random.Random(23)
        for _ in range(150):
            vs = list(range(7))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.35]
            c = ex.cover_by_matching(es)
            self.assertTrue(all(a in c or b in c for a, b in es))
            self.assertLessEqual(len(c), 2 * len(ex.smallest_cover(vs, es)))
            sizes = [r.randint(1, 10) for _ in range(r.randint(1, 6))]
            self.assertLessEqual(len(ex.first_fit_decreasing(sizes, 10)), 11 * ex.fewest_bins(sizes, 10) // 9 + 1)


class TestDepth(unittest.TestCase):
    def test_metric_tsp(self) -> None:
        d = ex.travel_times(ex.TOWN, ex.TIMED)
        self.assertEqual(ex.best_tour(ex.TOWN, d)[0], 33)
        self.assertEqual((ex.mst(ex.TOWN, d)[1], ex.tree_doubling_tour(ex.TOWN, d)[1], ex.christofides(ex.TOWN, d)[1]), (25, 40, 40))
        r = random.Random(27)
        for _ in range(60):
            n = r.randint(3, 7)
            pts = [(r.randint(0, 50), r.randint(0, 50)) for _ in range(n)]
            vs = list(range(n))
            import math
            dd = {(a, b): math.dist(pts[a], pts[b]) for a in vs for b in vs}
            opt = ex.best_tour(vs, dd)[0]
            t, L, w = ex.tree_doubling_tour(vs, dd)
            ct, cl = ex.christofides(vs, dd)
            self.assertEqual((sorted(t), sorted(ct)), (vs, vs))
            self.assertLessEqual(w, opt + 1e-9)
            self.assertLessEqual(L, 2 * opt + 1e-9)
            self.assertLessEqual(cl, 1.5 * opt + 1e-9)

    def test_set_cover_and_scheduling(self) -> None:
        self.assertEqual((ex.greedy_set_cover(ex.TITLES, ex.GRID_SETS), ex.best_set_cover(ex.TITLES, ex.GRID_SETS)),
                         (["block 1", "block 2", "block 3"], ["row A", "row B"]))
        self.assertEqual(round(ex.harmonic(14), 2), 3.25)
        r = random.Random(28)
        for _ in range(150):
            uni = set(range(r.randint(1, 8)))
            sets = {f"s{i}": {x for x in uni if r.random() < 0.4} for i in range(r.randint(1, 6))}
            sets["all"] = set(uni) if r.random() < 0.2 else sets.get("s0", set()) | uni
            g, b = ex.greedy_set_cover(uni, sets), ex.best_set_cover(uni, sets)
            self.assertLessEqual(len(g), ex.harmonic(len(uni)) * len(b) + 1e-9)
        self.assertEqual((ex.list_schedule([2, 3, 4, 6, 2, 2], 3)[0], ex.lpt_schedule([2, 3, 4, 6, 2, 2], 3)[0], ex.best_makespan([2, 3, 4, 6, 2, 2], 3)), (8, 7, 7))
        self.assertEqual((ex.list_schedule([1] * 6 + [3], 3)[0], ex.best_makespan([1] * 6 + [3], 3)), (5, 3))
        self.assertEqual((ex.lpt_schedule([3, 3, 2, 2, 2], 2)[0], ex.best_makespan([3, 3, 2, 2, 2], 2)), (7, 6))
        for _ in range(150):
            m = r.randint(1, 3)
            jobs = [r.randint(1, 9) for _ in range(r.randint(1, 7))]
            opt = ex.best_makespan(jobs, m)
            self.assertLessEqual(ex.list_schedule(jobs, m)[0], (2 - 1 / m) * opt + 1e-9)
            self.assertLessEqual(ex.lpt_schedule(jobs, m)[0], (4 / 3 - 1 / (3 * m)) * opt + 1e-9)

    def test_k_centre_and_knapsack(self) -> None:
        c, rad = ex.greedy_k_centre(ex.HOMES, 3)
        self.assertEqual((c, round(rad, 3), round(ex.best_k_centre(ex.HOMES, 3), 3)), ([(1, 1), (9, 7), (8, 1)], 5.099, 4.123))
        r = random.Random(29)
        for _ in range(100):
            pts = list({(r.randint(0, 20), r.randint(0, 20)) for _ in range(r.randint(2, 9))})
            k = r.randint(1, len(pts))
            self.assertLessEqual(ex.greedy_k_centre(pts, k)[1], 2 * ex.best_k_centre(pts, k) + 1e-9)
        self.assertEqual(ex.knapsack_exact(ex.SHELF_VALUES, ex.SHELF_WEIGHTS, 20), 3658)
        self.assertEqual(ex.knapsack_fptas(ex.SHELF_VALUES, ex.SHELF_WEIGHTS, 20, 0.5)[::2], (3658, 109))
        for _ in range(150):
            n = r.randint(1, 8)
            vals = [r.randint(1, 300) for _ in range(n)]
            wts = [r.randint(1, 15) for _ in range(n)]
            cap = r.randint(0, 40)
            best = ex.knapsack_exact(vals, wts, cap)
            for eps in (0.5, 0.2):
                v, chosen, _ = ex.knapsack_fptas(vals, wts, cap, eps)
                self.assertLessEqual(sum(wts[i] for i in chosen), cap)
                self.assertGreaterEqual(v, (1 - eps) * best - 1e-9)


    def test_max3sat(self) -> None:
        import itertools
        import random
        r = random.Random(26)
        for _ in range(60):
            n = r.randint(3, 7)
            clauses = [[v * r.choice([1, -1]) for v in r.sample(range(1, n + 1), 3)] for _ in range(r.randint(1, 16))]
            best = max(sum(any(dict(zip(range(1, n + 1), bits))[abs(l)] == (l > 0) for l in c) for c in clauses)
                       for bits in itertools.product([True, False], repeat=n))
            d, _ = ex.max3sat_derandomized(clauses, n)
            self.assertGreaterEqual(d, 7 * len(clauses) / 8)
            self.assertLessEqual(d, best)
            got, s = ex.max3sat_random(clauses, n, tries=20)
            self.assertLessEqual(got, best)


if __name__ == "__main__":
    unittest.main()
