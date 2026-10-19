import itertools
import random
import unittest
from fractions import Fraction

import ch09_examples as ex
import ch09_solutions as sol


def brute_lp(c, a, b):
    """Best vertex: choose n tight constraints among A x <= b and x >= 0, solve exactly, keep feasible ones."""
    n = len(c)
    rows = [([Fraction(v) for v in r], Fraction(bi)) for r, bi in zip(a, b)]
    rows += [([Fraction(-1 if j == i else 0) for j in range(n)], Fraction(0)) for i in range(n)]
    best = None
    for combo in itertools.combinations(rows, n):
        m = [r[:] + [bi] for r, bi in combo]
        ok = True
        for col in range(n):
            piv = next((i for i in range(col, n) if m[i][col] != 0), None)
            if piv is None:
                ok = False
                break
            m[col], m[piv] = m[piv], m[col]
            for i in range(n):
                if i != col and m[i][col] != 0:
                    f = m[i][col] / m[col][col]
                    m[i] = [x - f * y for x, y in zip(m[i], m[col])]
        if not ok:
            continue
        x = [m[i][n] / m[i][i] for i in range(n)]
        if all(sum(r[j] * x[j] for j in range(n)) <= bi for r, bi in rows):
            val = sum(Fraction(ci) * xi for ci, xi in zip(c, x))
            best = val if best is None else max(best, val)
    return best


class TestLP(unittest.TestCase):
    def test_against_vertices(self) -> None:
        rng = random.Random(1)
        for _ in range(80):
            n = rng.randint(2, 3)
            m = rng.randint(1, 4)
            c = [rng.randint(0, 9) for _ in range(n)]
            a = [[rng.randint(1, 6) for _ in range(n)] for _ in range(m)]
            b = [rng.randint(1, 30) for _ in range(m)]
            value, x = ex.simplex(c, a, b)
            self.assertAlmostEqual(value, float(brute_lp(c, a, b)), places=6)
            self.assertTrue(sol.is_feasible(tuple(x), a, b))
            self.assertAlmostEqual(sum(ci * xi for ci, xi in zip(c, x)), value, places=6)
            if n == 2:
                cons = [(a[i][0], a[i][1], b[i]) for i in range(m)] + [(-1, 0, 0), (0, -1, 0)]
                self.assertAlmostEqual(float(ex.solve_2d((c[0], c[1]), cons)[0]), value, places=6)

    def test_examples(self) -> None:
        self.assertEqual(ex.factory_plan(), (Fraction(1900), (Fraction(30), Fraction(20))))
        self.assertEqual(sol.diet_problem(), (Fraction(62, 7), (Fraction(16, 7), Fraction(10, 7))))
        value, x = sol.best_mix([5, 4], [[6, 4], [1, 2]], [24, 6])
        self.assertAlmostEqual(value, 21)
        with self.assertRaises(ValueError):
            ex.simplex([1, 1], [[1, -1]], [1])


if __name__ == "__main__":
    unittest.main()
