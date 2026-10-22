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


class TestDepth(unittest.TestCase):
    def test_spf_and_factorising(self) -> None:
        spf, writes = ex.smallest_factor_sieve(10_000)
        self.assertEqual(spf[2:13], [2, 3, 2, 5, 2, 7, 2, 3, 2, 11, 2])
        self.assertEqual(writes, 10_000 - 1229 - 1)                     # each composite written once
        self.assertEqual(ex.factorise_with_spf(360, spf), [2, 2, 2, 3, 3, 5])
        self.assertEqual(ex.factorise_steps(360), [(2, 180), (2, 90), (2, 45), (3, 15), (3, 5), (5, 1)])
        self.assertEqual((ex.factorise_steps(1), ex.factorise_with_spf(1, spf)), ([], []))
        self.assertEqual(ex.smallest_factor_sieve(1), ([0, 0], 0))
        for n in range(1, 10_001):
            self.assertEqual(ex.factorise_with_spf(n, spf), ex.factorise(n))

    def test_segmented_and_mertens(self) -> None:
        self.assertEqual(ex.segmented_sieve(1, 50), ex.sieve(50)[0])
        self.assertEqual((ex.segmented_sieve(14, 16), ex.segmented_sieve(0, 1), ex.segmented_sieve(10, 5)), ([], [], []))
        self.assertEqual(ex.segmented_sieve(1000, 1100), [p for p in ex.sieve(1100)[0] if p >= 1000])
        self.assertEqual(len(ex.segmented_sieve(10 ** 12, 10 ** 12 + 1000)), 37)
        self.assertAlmostEqual(ex.reciprocal_prime_sum(1000), 2.1981, places=4)


if __name__ == "__main__":
    unittest.main()
