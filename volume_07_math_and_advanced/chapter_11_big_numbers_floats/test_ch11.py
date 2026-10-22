import math
import unittest
from fractions import Fraction

import ch11_examples as ex


class TestChapter11(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual([ex.wrap(n) for n in (127, 128, 200, -1, 300)], [127, -128, -56, -1, 44])
        self.assertEqual((0.1 + 0.2 == 0.3, ex.close(0.1 + 0.2, 0.3), ex.add_tenths(10)), (False, True, 0.9999999999999999))
        big = [1e16] + [1.0] * 10000
        self.assertEqual((ex.naive_sum(big) - 1e16, ex.kahan_sum(big) - 1e16, math.fsum(big) - 1e16), (0.0, 10000.0, 10000.0))

    def test_every_case(self) -> None:
        self.assertTrue(2.0 ** 53 + 1 == 2.0 ** 53)
        self.assertEqual(Fraction(1, 10) + Fraction(2, 10), Fraction(3, 10))
        self.assertEqual(1e308 * 10, math.inf)
        self.assertTrue(math.isnan(math.inf - math.inf))
        self.assertEqual((ex.naive_sum([]), ex.kahan_sum([]), ex.wrap(0), ex.wrap(255)), (0.0, 0.0, 0, -1))
        self.assertEqual(len(str(2 ** 100)), 31)


class TestDepth(unittest.TestCase):
    def test_twos_complement(self) -> None:
        self.assertEqual((ex.bits_of(5), ex.bits_of(-5), ex.negate_pattern("00000101"), ex.signed_value("11111011")),
                         ("00000101", "11111011", "11111011", -5))
        self.assertEqual((ex.bits_of(-128), ex.negate_pattern("10000000")), ("10000000", "10000000"))     # -(-128) wraps
        for n in range(-128, 128):
            self.assertEqual(ex.signed_value(ex.bits_of(n)), n)
            if n != -128:
                self.assertEqual(ex.signed_value(ex.negate_pattern(ex.bits_of(n))), -n)
            self.assertEqual(n & -n if n > 0 else 0, (n & -n) if n > 0 else 0)
        self.assertEqual(ex.add_in_register(2 ** 31 - 1, 1), -2 ** 31)
        self.assertEqual((ex.midpoint_unsafe(2 ** 30 + 5, 2 ** 31 - 3), ex.midpoint_safe(2 ** 30 + 5, 2 ** 31 - 3)), (-536870911, 1610612737))
        self.assertEqual((ex.shift_right_arithmetic(-8, 1), ex.shift_right_logical(-8, 1)), (-4, 124))

    def test_chapter_numbers(self) -> None:
        self.assertEqual((ex.bits_of(-3), ex.float_parts(4.0), ex.wrap(129)), ("11111101", (0, 1025, 0), -127))
        self.assertEqual(((1e16 + -1e16) + 1.0, 1e16 + (-1e16 + 1.0)), (1.0, 0.0))
        self.assertEqual(Fraction(0.1), Fraction(3602879701896397, 2 ** 55))

    def test_floats(self) -> None:
        self.assertEqual([ex.float_parts(x) for x in (1.0, 0.1, -2.5, 2.0 ** -1074, float("inf"))],
                         [(0, 1023, 0), (0, 1019, 2702159776422298), (1, 1024, 1125899906842624), (0, 0, 1), (0, 2047, 0)])
        for x in (1.0, 0.1, -2.5, 1e300, 3.14159):
            self.assertEqual(float(ex.float_value_from_parts(*ex.float_parts(x))), x)
        self.assertEqual((math.ulp(1.0), ex.sys_float_epsilon()), (2 ** -52, 2 ** -52))
        self.assertEqual((ex.one_minus_cos_naive(1e-8), ex.one_minus_cos_stable(1e-8)), (0.0, 0.5))
        self.assertEqual((ex.small_root_naive(1e8, 1.0), ex.small_root_stable(1e8, 1.0)), (7.450580596923828e-09, 1e-08))
        rows = ex.kahan_trace([1e16, 1.0, 1.0, 1.0, 1.0])
        self.assertEqual((rows[1][3], rows[-1][2]), (-1.0, 1e16 + 4))
        self.assertEqual(ex.kahan_trace([]), [])
        self.assertFalse(float("nan") == float("nan"))


if __name__ == "__main__":
    unittest.main()
