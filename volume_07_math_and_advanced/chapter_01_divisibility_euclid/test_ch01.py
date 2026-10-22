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


class TestDepth(unittest.TestCase):
    def test_tiling_and_lame(self) -> None:
        self.assertEqual(ex.tiling(84, 36), [(36, 2), (12, 3)])
        self.assertEqual(ex.tiling(1071, 462), [(462, 2), (147, 3), (21, 7)])
        self.assertEqual(ex.tiling(21, 13), [(13, 1), (8, 1), (5, 1), (3, 1), (2, 1), (1, 2)])
        self.assertEqual(ex.tiling(5, 0), [])
        self.assertEqual((ex.fibonacci(29), ex.fibonacci(30)), (514229, 832040))
        self.assertEqual((ex.worst_pair_below(1000), ex.worst_pair_below(100)), ((14, 987, 610), (9, 89, 55)))
        self.assertEqual(round(ex.lame_bound(514229), 2), 28.33)
        r = random.Random(2)
        for _ in range(300):
            a, b = r.randint(2, 10 ** 9), r.randint(1, 10 ** 9)
            a, b = max(a, b) + 1, min(a, b)
            self.assertLessEqual(ex.euclid_steps(a, b), ex.lame_bound(b) + 1e-9)
            self.assertEqual(ex.gcd_recursive(a, b), math.gcd(a, b))

    def test_many_and_lcm(self) -> None:
        self.assertEqual((ex.gcd_many([84, 36, 60]), ex.gcd_many([]), ex.gcd_many([0, 0]), ex.gcd_many([7])), (12, 0, 0, 7))
        self.assertEqual((ex.lcm_many([12, 18, 30]), ex.lcm_many([]), ex.lcm(-4, 6)), (180, 1, 12))
        self.assertEqual(ex.lcm(2 ** 40, 3 ** 30), 2 ** 40 * 3 ** 30)


if __name__ == "__main__":
    unittest.main()
