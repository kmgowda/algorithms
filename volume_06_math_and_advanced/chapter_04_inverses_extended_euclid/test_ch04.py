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


if __name__ == "__main__":
    unittest.main()
