import math
import unittest

import ch02_examples as ex


class TestChapter2(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(ex.sieve(50), ([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47], 45))
        self.assertEqual((ex.is_prime(97), ex.is_prime(91), ex.is_prime(1_000_003)), ((True, 8), (False, 6), (True, 999)))
        self.assertEqual((ex.factorise(84), ex.factorise(720720)), ([2, 2, 3, 7], [2, 2, 2, 2, 3, 3, 5, 7, 11, 13]))
        self.assertEqual([(len(p), c) for p, c in (ex.sieve(100), ex.sieve(10_000))], [(25, 104), (1229, 16981)])
        self.assertEqual(len(ex.sieve(1_000_000)[0]), 78498)

    def test_every_case(self) -> None:
        self.assertEqual([ex.is_prime(n) for n in (0, 1, 2, 4)], [(False, 0), (False, 0), (True, 0), (False, 1)])
        self.assertEqual((ex.sieve(1), ex.sieve(2), ex.factorise(1), ex.factorise(97)), (([], 0), ([2], 0), [], [97]))
        self.assertEqual(ex.is_prime(2 ** 31 - 1), (True, 46339))
        with self.assertRaises(ValueError):
            ex.factorise(0)
        self.assertEqual((ex.is_prime(221)[0], ex.factorise(360), ex.sieve(30)[0]), (False, [2, 2, 2, 3, 3, 5], [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]))
        primes = set(ex.sieve(2000)[0])
        for n in range(2000):
            self.assertEqual(ex.is_prime(n)[0], n in primes)
            if n:
                self.assertEqual(math.prod(ex.factorise(n)), n)


if __name__ == "__main__":
    unittest.main()
