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


if __name__ == "__main__":
    unittest.main()
