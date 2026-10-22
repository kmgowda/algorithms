import random
import unittest

import ch03_examples as ex


class TestChapter3(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual((ex.clock(9, 5), ex.clock(11, 25), ex.clock(3, -5)), (2, 0, 10))
        self.assertEqual((ex.last_digit_table(7), ex.last_digit_table(3)), ([7, 9, 3, 1] * 2, [3, 9, 7, 1] * 2))
        self.assertEqual((ex.power_mod_naive(7, 100, 10), ex.power_mod(7, 100, 10), ex.power_mod(3, 1000, 1000007)), ((1, 100), (1, 9), (297623, 15)))
        self.assertEqual(ex.power_mod(2, 10 ** 18, 10 ** 9 + 7), (719476260, 83))

    def test_every_case(self) -> None:
        self.assertEqual([ex.power_mod(*a) for a in ((5, 0, 7), (5, 3, 1), (0, 0, 7), (-2, 3, 7))], [(1, 0), (0, 3), (1, 0), (6, 3)])
        for a in ((5, -1, 7), (5, 3, 0)):
            with self.assertRaises(ValueError):
                ex.power_mod(*a)
        self.assertEqual((ex.power_mod(10, 100, 7)[0], ex.power_mod(3, 13, 7)[0], ex.power_mod(3, 6, 7)[0], ex.last_digit_table(3, 4)[-1]), (4, 3, 1, 1))
        r = random.Random(3)
        for _ in range(300):
            b, e, m = r.randint(-50, 50), r.randint(0, 500), r.randint(1, 1000)
            self.assertEqual(ex.power_mod(b, e, m)[0], pow(b, e, m))


class TestDepth(unittest.TestCase):
    def test_trace_and_fermat(self) -> None:
        self.assertEqual(ex.power_mod_trace(3, 13, 7), [(1, 3, 3), (0, 2, 3), (1, 4, 5), (1, 2, 3)])
        self.assertEqual((ex.power_mod_trace(5, 0, 7), ex.power_mod_trace(5, 1, 7)), ([], [(1, 5, 5)]))
        self.assertEqual(ex.residue_row(3, 7), [3, 6, 2, 5, 1, 4])
        for p in (2, 3, 5, 7, 11, 13, 97):
            for a in range(1, p):
                self.assertEqual(sorted(ex.residue_row(a, p)), list(range(1, p)))
                self.assertEqual(pow(a, p - 1, p), 1)
        self.assertEqual(ex.residue_row(2, 6), [2, 4, 0, 2, 4])

    def test_phi_and_euler(self) -> None:
        self.assertEqual((ex.phi(3233), ex.phi(12), ex.phi(7), ex.phi(1), ex.phi(2 ** 10)), (3120, 4, 6, 1, 512))
        from math import gcd
        for n in range(1, 300):
            self.assertEqual(ex.phi(n), ex.phi_by_counting(n))
            for a in range(1, n):
                if gcd(a, n) == 1:
                    self.assertEqual(pow(a, ex.phi(n), n), 1 % n)
        with self.assertRaises(ValueError):
            ex.phi(0)

    def test_chapter_numbers(self) -> None:
        self.assertEqual([ex.power_mod(5, 11, 13)[0], ex.power_mod(7, 2026, 12)[0], ex.power_mod(7, 7 ** 7, 10)[0],
                          ex.power_mod(2, 100, 11)[0], ex.power_mod(10, 100, 7)[0]], [8, 1, 3, 1, 4])
        self.assertEqual((ex.phi(15), ex.phi(97), [3 * k % 9 for k in range(1, 9)]), (8, 96, [3, 6, 0, 3, 6, 0, 3, 6]))

    def test_mulmod(self) -> None:
        r = random.Random(3)
        for _ in range(300):
            m = r.randint(1, 2 ** 64)
            a, b = r.randint(0, 2 ** 64), r.randint(0, 2 ** 64)
            self.assertEqual(ex.mul_mod_by_doubling(a, b, m), a * b % m)
        self.assertEqual(round(ex.average_multiplications(1_000_000, 1_001_000), 1), 29.6)


if __name__ == "__main__":
    unittest.main()
