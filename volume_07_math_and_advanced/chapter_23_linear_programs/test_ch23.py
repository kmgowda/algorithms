import itertools
import random
import unittest
from fractions import Fraction

import ch23_examples as ex


class TestChapter23(unittest.TestCase):
    def test_library(self) -> None:
        cs = ex.corners(ex.LIBRARY_A, ex.LIBRARY_B)
        self.assertEqual(sorted(tuple(map(int, x)) for x in cs), [(0, 0), (0, 40), (15, 35), (30, 20), (40, 0)])
        value, x = ex.best_corner(ex.LIBRARY_A, ex.LIBRARY_B, ex.LIBRARY_C)
        self.assertEqual((value, x), (130, [30, 20]))
        self.assertEqual(ex.slacks(ex.LIBRARY_A, ex.LIBRARY_B, x), [0, 0, 30])
        self.assertEqual(ex.tight(ex.LIBRARY_A, ex.LIBRARY_B, x), [0, 1])
        # loans at each corner, as drawn in the chapter
        self.assertEqual(sorted(3 * a + 2 * b for a, b in cs), [0, 80, 115, 120, 130])

    def test_every_case(self) -> None:
        # a whole edge of best plans: loans 2x + 2y tie along the slots rule
        self.assertEqual(ex.best_corner(ex.LIBRARY_A, ex.LIBRARY_B, [2, 2])[0], 100)
        tied = [x for x in ex.corners(ex.LIBRARY_A, ex.LIBRARY_B) if 2 * x[0] + 2 * x[1] == 100]
        self.assertEqual(sorted(tuple(map(int, x)) for x in tied), [(15, 35), (30, 20)])
        # infeasible: at least 45 paperbacks but cataloguing allows 40
        self.assertEqual(ex.corners(ex.LIBRARY_A + [[0, -1]], ex.LIBRARY_B + [-45]), [])
        self.assertIsNone(ex.best_corner(ex.LIBRARY_A + [[0, -1]], ex.LIBRARY_B + [-45], ex.LIBRARY_C))
        # unbounded region: corners exist but the best corner is not the answer (checked in Chapter 24)
        self.assertEqual(ex.corners([[1, -1]], [2]), [[2, 0], [0, 0]])
        # best at the origin; a degenerate corner where three lines meet
        self.assertEqual(ex.best_corner(ex.LIBRARY_A, ex.LIBRARY_B, [-1, -1]), (0, [0, 0]))
        A, b = [[1, 1], [1, 0], [0, 1]], [2, 1, 1]
        self.assertEqual(ex.tight(A, b, [1, 1]), [0, 1, 2])
        # no rules at all: only the origin
        self.assertEqual(ex.corners([], []), [[]])
        self.assertEqual(ex.best_corner([[1]], [5], [1]), (5, [5]))

    def test_standard_form(self) -> None:
        A, b, c = ex.to_standard_form([1, 1], [([1, 2], ">=", 4), ([3, 1], "=", 6)], minimise=True)
        self.assertEqual((A, b, c), ([[-1, -2], [3, 1], [-3, -1]], [-4, 6, -6], [-1, -1]))
        A, b, c = ex.to_standard_form([1, 1], [([1, 1], "<=", 3)], free=(1,))
        self.assertEqual((A, b, c), ([[1, 1, -1]], [3], [1, 1, -1]))

    def test_integer_programs(self) -> None:
        self.assertEqual(ex.best_corner(ex.CASES_A, ex.CASES_B, ex.CASES_C), (21, [3, Fraction(3, 2)]))
        self.assertEqual(ex.best_integer_plan(ex.CASES_A, ex.CASES_B, ex.CASES_C, 6), (20, [4, 0]))
        self.assertFalse(ex.feasible(ex.CASES_A, ex.CASES_B, [3, 2]))
        self.assertEqual(ex.slacks(ex.CASES_A, ex.CASES_B, [3, 1]), [2, 1])

    def test_cover_reduction(self) -> None:
        r = random.Random(23)
        for _ in range(60):
            vs = list(range(6))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.4]
            best = next(k for k in range(7) if any(all(a in g or b in g for a, b in es)
                                                  for g in itertools.combinations(vs, k)))
            for k in range(7):
                ok = ex.zero_one_feasible(*ex.cover_as_ip(vs, es, k), len(vs)) is not None
                self.assertEqual(ok, k >= best)

    def test_random_against_brute_force(self) -> None:
        r = random.Random(7)
        for _ in range(100):
            A = [[r.randint(1, 6), r.randint(1, 6)] for _ in range(3)]
            b = [r.randint(5, 30) for _ in range(3)]
            c = [r.randint(0, 5), r.randint(0, 5)]
            value, x = ex.best_corner(A, b, c)
            self.assertTrue(ex.feasible(A, b, x))
            grid = [(Fraction(i, 2), Fraction(j, 2)) for i in range(61) for j in range(61)]
            self.assertTrue(all(c[0] * p + c[1] * q <= value for p, q in grid if ex.feasible(A, b, (p, q))))


if __name__ == "__main__":
    unittest.main()
