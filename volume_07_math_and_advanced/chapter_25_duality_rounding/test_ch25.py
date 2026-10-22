import itertools
import random
import unittest
from fractions import Fraction

import ch25_examples as ex


class TestChapter25(unittest.TestCase):
    def test_library_dual(self) -> None:
        primal = ex.simplex(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C)
        d = ex.simplex(*ex.dual(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C))
        self.assertEqual((d["x"], -d["value"]), ([1, 1, 0], 130))
        self.assertEqual(primal["duals"], d["x"])                 # the final tableau already holds the prices
        self.assertTrue(ex.is_certificate(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C, primal["x"], d["x"]))
        self.assertTrue(ex.complementary_slackness(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C, primal["x"], d["x"]))
        # weak duality: any plan's loans <= any price list's total
        self.assertLessEqual(ex.objective(ex.LIBRARY_C, [15, 35]), ex.objective(ex.LIBRARY_B, [3, 0, 0]))
        self.assertFalse(ex.complementary_slackness(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C, [15, 35], [1, 1, 0]))

    def test_dual_of_dual(self) -> None:
        A, b, c = ex.dual(*ex.dual(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C))
        self.assertEqual((A, b, c), (ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C))

    def test_strong_duality_random(self) -> None:
        r = random.Random(25)
        for _ in range(150):
            m, n = r.randint(1, 4), r.randint(1, 4)
            A = [[r.randint(-1, 5) for _ in range(n)] for _ in range(m)]
            b = [r.randint(-2, 12) for _ in range(m)]
            c = [r.randint(-2, 6) for _ in range(n)]
            p, d = ex.simplex(A, b, c), ex.simplex(*ex.dual(A, b, c))
            if p["status"] == "optimal":
                self.assertEqual((d["status"], -d["value"]), ("optimal", p["value"]))
                self.assertTrue(ex.complementary_slackness(A, b, c, p["x"], d["x"]))
                self.assertTrue(ex.is_certificate(A, b, c, p["x"], p["duals"]))   # the tableau's prices are optimal
            elif p["status"] == "unbounded":
                self.assertEqual(d["status"], "infeasible")
            else:
                self.assertIn(d["status"], ("infeasible", "unbounded"))

    def test_town_cover(self) -> None:
        lp, x = ex.cover_lp(ex.TOWN, ex.ROADS, ex.WAGE)
        self.assertEqual(lp, 18)
        self.assertTrue(all(v in (0, Fraction(1, 2), 1) for v in x.values()))
        rounded = ex.round_cover(x)
        self.assertEqual(sum(ex.WAGE[v] for v in rounded), 30)
        self.assertTrue(all(a in rounded or b in rounded for a, b in ex.ROADS))
        self.assertEqual(ex.best_weighted_cover(ex.TOWN, ex.ROADS, ex.WAGE)[0], 20)
        cover, price = ex.pricing_cover(ex.ROADS, ex.WAGE)
        self.assertEqual((sum(ex.WAGE[v] for v in cover), sum(price.values())), (23, 14))

    def test_every_case(self) -> None:
        tri = [("a", "b"), ("b", "c"), ("a", "c")]
        one = {v: 1 for v in "abc"}
        self.assertEqual(ex.cover_lp(list("abc"), tri, one), (Fraction(3, 2), {v: Fraction(1, 2) for v in "abc"}))
        self.assertEqual(ex.best_weighted_cover(list("abc"), tri, one)[0], 2)
        self.assertEqual(ex.cover_lp(["a"], [], {"a": 5}), (0, {"a": 0}))          # no roads: no wardens
        self.assertEqual(ex.round_cover(ex.cover_lp(["a", "b"], [("a", "b")], {"a": 1, "b": 3})[1]), ["a"])
        for n in range(3, 7):                                                      # complete graphs: gap 2 - 2/n
            vs = list(range(n))
            lp, _ = ex.cover_lp(vs, list(itertools.combinations(vs, 2)), {v: 1 for v in vs})
            self.assertEqual(lp, Fraction(n, 2))
        # both a program and its dual can be infeasible
        A, b, c = [[1, -1], [-1, 1]], [1, -2], [2, -1]
        self.assertEqual((ex.simplex(A, b, c)["status"], ex.simplex(*ex.dual(A, b, c))["status"]),
                         ("infeasible", "infeasible"))

    def test_rounding_random(self) -> None:
        r = random.Random(52)
        for _ in range(80):
            vs = list(range(6))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.45]
            cost = {v: r.randint(1, 9) for v in vs}
            lp, x = ex.cover_lp(vs, es, cost)
            cover = ex.round_cover(x)
            best = ex.best_weighted_cover(vs, es, cost)[0]
            self.assertTrue(all(a in cover or b in cover for a, b in es))
            self.assertLessEqual(lp, best)
            self.assertLessEqual(sum(cost[v] for v in cover), 2 * lp)
            pc, price = ex.pricing_cover(es, cost)
            self.assertTrue(all(a in pc or b in pc for a, b in es))
            self.assertLessEqual(sum(cost[v] for v in pc), 2 * sum(price.values()))


if __name__ == "__main__":
    unittest.main()
