import random
import unittest

import ch18_examples as ex


class TestChapter18(unittest.TestCase):
    def test_examples(self) -> None:
        rng = random.Random(18)
        pile = [58, 25, 91, 12, 70, 47, 84, 31, 63]
        self.assertEqual((ex.quickselect(pile, 4, rng), ex.quickselect(pile, 4, rng, "first")), ((58, 27), (58, 9)))
        s = list(range(2000))
        self.assertEqual((ex.quickselect(s, 1000, rng, "first")[1], ex.quickselect(s, 1000, rng)[1]), (1501500, 7639))
        A, B, bad = [[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 51]]
        C = ex.matmul(A, B)
        self.assertEqual((C, ex.freivalds(A, B, C, 10, rng), ex.freivalds(A, B, bad, 10, rng)), ([[19, 22], [43, 50]], True, False))
        self.assertEqual(sum(ex.freivalds(A, B, bad, 1, random.Random(s)) for s in range(1000)), 495)

    def test_every_case(self) -> None:
        r = random.Random(1)
        self.assertEqual((ex.quickselect([5], 0, r), ex.quickselect([2, 2, 2], 1, r)[0], ex.quickselect([3, 1, 2], 2, r)[0]), ((5, 1), 2, 3))
        with self.assertRaises(ValueError):
            ex.quickselect([], 0, r)
        for _ in range(300):
            v = [r.randint(0, 20) for _ in range(r.randint(1, 15))]
            k = r.randrange(len(v))
            self.assertEqual(ex.quickselect(v, k, r)[0], sorted(v)[k])


class TestDepth(unittest.TestCase):
    def test_toolkit(self) -> None:
        from fractions import Fraction
        for n in range(1, 7):
            self.assertEqual(ex.fixed_points_exact(n)[0], Fraction(1))
        b = ex.tail_bounds(100, 0.6)
        self.assertTrue(b["exact"] <= b["chernoff"] <= b["markov"])
        self.assertTrue(b["exact"] <= b["chebyshev"])
        self.assertEqual(f"{ex.tail_bounds(1000, 0.6)['exact']:.3g}", "1.36e-10")
        self.assertAlmostEqual(ex.trials_until_success(0.25, 20000, 4), 4, delta=0.1)

    def test_karger(self) -> None:
        self.assertEqual((len(ex.CABLES), ex.min_cut_brute(ex.ROOMS, ex.CABLES)), (14, 2))
        self.assertEqual(ex.karger(ex.ROOMS, ex.CABLES, 1000, 8), (2, 212))
        self.assertEqual((ex.min_cut_brute(ex.TOWN, ex.ROADS), ex.karger(ex.TOWN, ex.ROADS, 1000, 6)), (2, (2, 515)))
        import random as rnd
        r = rnd.Random(19)
        for _ in range(60):
            n = r.randint(2, 8)
            vs = list(range(n))
            es = [(i, i + 1) for i in range(n - 1)] + [(r.randrange(n), r.randrange(n)) for _ in range(r.randint(0, 10))]
            es = [(a, b) for a, b in es if a != b]
            best, hits = ex.karger(vs, es, 300, r.randint(0, 99))
            self.assertEqual(best, ex.min_cut_brute(vs, es))
            cut, side = ex.karger_once(vs, es, r)
            self.assertTrue(0 < len(side) < n)
            self.assertEqual(cut, sum(1 for a, b in es if (a in side) != (b in side)))


if __name__ == "__main__":
    unittest.main()
