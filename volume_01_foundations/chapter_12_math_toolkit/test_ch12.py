import math
import unittest

import ch12_examples as ex


class TestChapter12(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual([ex.gauss_sum(n) for n in (0, 1, 2, 10, 100)], [0, 1, 3, 55, 5050])
        self.assertEqual([ex.powers_of_two_sum(k) for k in (0, 1, 2, 5, 10)], [0, 1, 3, 31, 1023])
        self.assertEqual([ex.halving_total(s) for s in (0, 1, 3, 8, 1000, 1024)], [0, 1, 4, 15, 1994, 2047])
        for s in range(1, 3000):
            self.assertLess(ex.halving_total(s), 2 * s)

    def test_formulas(self) -> None:
        self.assertTrue(all(ex.check_formulas(n) for n in range(1, 400)))
        self.assertEqual(ex.gauss_sum(100), 5050)
        self.assertEqual(ex.powers_of_two_sum(10), 1023)
        self.assertEqual(ex.halving_total(1000), 1994)
        for s in range(1, 3000):
            self.assertLess(ex.halving_total(s), 2 * s)
        self.assertEqual((math.floor(math.log2(100)), math.ceil(math.log2(100))), (6, 7))

    def test_geometric_sum(self) -> None:
        self.assertEqual([ex.geometric_sum(2, n) for n in (-1, 0, 1, 4, 9)], [0, 1, 3, 31, 1023])
        self.assertEqual((ex.geometric_sum(3, 4), ex.geometric_sum(10, 3), ex.geometric_sum(1, 5)), (121, 1111, 6))
        for x in range(0, 6):
            for n in range(0, 12):
                self.assertEqual(ex.geometric_sum(x, n), sum(x ** i for i in range(n + 1)))

    def test_log_factorial(self) -> None:
        self.assertEqual((ex.log2_factorial(0), ex.log2_factorial(1)), (0, 0))
        self.assertAlmostEqual(ex.log2_factorial(16), math.log2(math.factorial(16)))
        for n in range(2, 300):
            lf = ex.log2_factorial(n)
            self.assertLessEqual(lf, n * math.log2(n))
            self.assertGreaterEqual(lf, (n / 2) * math.log2(n / 2))

    def test_harmonic(self) -> None:
        self.assertEqual((ex.harmonic(0), ex.harmonic(1), ex.harmonic_groups(0)), (0, 1, []))
        self.assertEqual(ex.harmonic_groups(1), [1])
        for n in range(1, 600):
            groups = ex.harmonic_groups(n)
            self.assertEqual(len(groups), n.bit_length())
            self.assertAlmostEqual(sum(groups), ex.harmonic(n))
            self.assertTrue(all(g <= 1 + 1e-12 for g in groups))
            self.assertTrue(all(g >= 0.5 - 1e-12 for g in groups[:-1]))
            self.assertLess(abs(ex.harmonic(n) - math.log(n) - 0.5772), 0.5)


if __name__ == "__main__":
    unittest.main()
