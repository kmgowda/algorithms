import math
import random
import unittest

import ch01_examples as ex


class TestChapter1(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(ex.divisors(36), [1, 2, 3, 4, 6, 9, 12, 18, 36])
        log = []
        self.assertEqual((ex.gcd(84, 36, log), log, ex.lcm(84, 36), ex.gcd_by_listing(84, 36)), (12, [(84, 36, 12), (36, 12, 0)], 252, 12))
        self.assertEqual((ex.gcd(1071, 462), ex.euclid_steps(1071, 462), ex.euclid_steps(832040, 514229)), (21, 3, 28))

    def test_every_case(self) -> None:
        self.assertEqual([ex.gcd(a, b) for a, b in ((0, 5), (5, 0), (0, 0), (-12, 18))], [5, 5, 0, 6])
        self.assertEqual((ex.lcm(0, 5), ex.lcm(4, 6), ex.divisors(1), ex.divisors(97), len(ex.divisors(720720))), (0, 12, [1], [1, 97], 240))
        with self.assertRaises(ValueError):
            ex.divisors(0)
        self.assertEqual((ex.divisors(28), ex.gcd(48, 18), ex.lcm(48, 18), ex.lcm(12, 18), ex.gcd(ex.gcd(84, 36), 60)), ([1, 2, 4, 7, 14, 28], 6, 144, 36, 12))
        r = random.Random(1)
        for _ in range(300):
            a, b = r.randint(0, 10 ** 6), r.randint(0, 10 ** 6)
            self.assertEqual(ex.gcd(a, b), math.gcd(a, b))


if __name__ == "__main__":
    unittest.main()
