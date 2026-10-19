import math
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


class TestNumberTheoryTwo(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(400):
            b, e, m = rng.randint(0, 10 ** 6), rng.randint(0, 10 ** 6), rng.randint(2, 10 ** 9)
            self.assertEqual(ex.fast_power(b, e, m), pow(b, e, m))
            a, c = rng.randint(1, 10 ** 6), rng.randint(1, 10 ** 6)
            g, x, y = ex.extended_gcd(a, c)
            self.assertEqual(g, math.gcd(a, c))
            self.assertEqual(a * x + c * y, g)
            m = rng.randint(2, 1000)
            if math.gcd(a, m) == 1:
                self.assertEqual(ex.mod_inverse(a, m) * a % m, 1 % m)
            else:
                with self.assertRaises(ValueError):
                    ex.mod_inverse(a, m)
            self.assertEqual(ex.mod_inverse_prime(a % 1009 or 1, 1009), pow(a % 1009 or 1, -1, 1009))
            xr, n = rng.uniform(0.5, 1.5), rng.randint(-20, 20)
            self.assertTrue(math.isclose(sol.my_pow(xr, n), xr ** n, rel_tol=1e-9))
            digits = [rng.randint(0, 9) for _ in range(rng.randint(1, 5))]
            self.assertEqual(sol.super_pow(a, digits), pow(a, int("".join(map(str, digits))), 1337))
            rs = [rng.randint(0, 2), rng.randint(0, 4), rng.randint(0, 6), rng.randint(0, 10)]
            x = sol.chinese_remainder(rs, [3, 5, 7, 11])
            self.assertTrue(0 <= x < 1155)
            self.assertEqual([x % 3, x % 5, x % 7, x % 11], rs)

    def test_examples(self) -> None:
        self.assertEqual(ex.mod_add(ex.MOD - 1, 5), 4)
        self.assertEqual(ex.mod_mul(10 ** 9, 10 ** 9), 10 ** 18 % ex.MOD)
        self.assertEqual(ex.extended_gcd(240, 46), (2, -9, 47))
        self.assertEqual(ex.mod_inverse(3, 11), 4)
        self.assertEqual(ex.day_of_week(0, 100), 2)
        self.assertTrue(ex.isbn10_valid("0-306-40615-2"))
        self.assertFalse(ex.isbn10_valid("0-306-40615-3"))
        self.assertEqual(sol.chinese_remainder([2, 3, 2], [3, 5, 7]), 23)


if __name__ == "__main__":
    unittest.main()
