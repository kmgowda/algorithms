import math
import random
import unittest

import ch04_examples as ex


class TestChapter4(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.extended_gcd(84, 36), ex.extended_gcd(240, 46)), ((12, 1, -2), (2, -9, 47)))
        self.assertEqual([ex.inverse(a, m) for a, m in ((3, 7), (7, 26), (4, 8), (17, 3120))], [5, 15, None, 2753])
        self.assertEqual((ex.solve_linear(3, 2, 7), ex.solve_linear(4, 2, 8)), ([3], []))

    def test_every_case(self) -> None:
        self.assertEqual([ex.inverse(a, m) for a, m in ((1, 1), (0, 7), (-3, 7), (10, 7))], [0, None, 2, 5])
        self.assertEqual((ex.extended_gcd(0, 5), ex.extended_gcd(5, 0)), ((5, 0, 1), (5, 1, 0)))
        with self.assertRaises(ValueError):
            ex.inverse(3, 0)
        self.assertEqual((ex.inverse(2, 7), ex.inverse(6, 9), 7 * 2 % 26, 14 * 15 % 26, pow(3, 5, 7), ex.solve_linear(4, 4, 8)), (4, None, 14, 2, 5, [1, 3, 5, 7]))
        r = random.Random(4)
        for _ in range(300):
            a, b = r.randint(-500, 500), r.randint(0, 500)
            g, x, y = ex.extended_gcd(a, b)
            self.assertEqual((g, a * x + b * y), (math.gcd(a, b), math.gcd(a, b)))
            m = r.randint(2, 60)
            self.assertEqual(ex.inverse(a, m), ex.inverse_by_search(a % m, m))


class TestDepth(unittest.TestCase):
    def test_table(self) -> None:
        rows = ex.extended_gcd_table(26, 7)
        self.assertEqual([r[:3] for r in rows], [(26, 1, 0), (7, 0, 1), (5, 1, -3), (2, -1, 4), (1, 3, -11), (0, -7, 26)])
        for r, s_, t, _ in rows:
            self.assertEqual(26 * s_ + 7 * t, r)
        self.assertEqual(ex.extended_gcd_table(5, 0), [(5, 1, 0, None), (0, 0, 1, None)])
        self.assertEqual((ex.extended_gcd_iterative(240, 46), ex.smallest_positive_combination(84, 36)), ((2, -9, 47), 12))
        import math
        r = __import__("random").Random(4)
        for _ in range(300):
            a, b = r.randint(0, 10 ** 6), r.randint(0, 10 ** 6)
            g, x, y = ex.extended_gcd_iterative(a, b)
            self.assertEqual((g, a * x + b * y), (math.gcd(a, b), math.gcd(a, b)))

    def test_congruences(self) -> None:
        self.assertEqual((ex.solve_congruence(4, 4, 8), ex.solve_congruence(6, 4, 10), ex.solve_congruence(4, 2, 8)),
                         ((1, 2, 4), (4, 5, 2), None))
        self.assertEqual(ex.solve_congruence(15, 6, 21), (6, 7, 3))
        for m in range(1, 40):
            for a in range(m):
                for b in range(m):
                    sol = ex.solve_congruence(a, b, m)
                    brute = ex.solve_linear(a, b, m)
                    expect = [] if sol is None else sorted(sol[0] + k * sol[1] for k in range(sol[2]))
                    self.assertEqual(brute, expect)

    def test_chapter_numbers(self) -> None:
        self.assertEqual([r[:3] for r in ex.extended_gcd_table(3120, 17)][:5], [(3120, 1, 0), (17, 0, 1), (9, 1, -183), (8, -1, 184), (1, 2, -367)])
        self.assertEqual((ex.inverse_by_fermat(5, 11), ex.solve_congruence(9, 6, 15), ex.inverses_up_to(11)[2:4]), (9, (4, 5, 3), [6, 4]))
        self.assertEqual([n for n in range(26) if ex.inverse(n, 26) is not None], [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25])

    def test_inverse_tables(self) -> None:
        self.assertEqual(ex.inverses_up_to(7), [0, 1, 4, 5, 2, 3, 6])
        for p in (2, 3, 5, 13, 97, 1009):
            inv = ex.inverses_up_to(p)
            for a in range(1, p):
                self.assertEqual(a * inv[a] % p, 1)
                self.assertEqual(ex.inverse_by_fermat(a, p), inv[a])


if __name__ == "__main__":
    unittest.main()
