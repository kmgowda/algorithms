import math
import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestNumberTheoryOne(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        primes = set(ex.sieve(3000))
        for n in range(3001):
            self.assertEqual(ex.is_prime(n), n in primes)
            if n < 400:
                self.assertEqual(ex.is_prime(n), n > 1 and all(n % d for d in range(2, n)))
        for _ in range(300):
            a, b = rng.randint(0, 10 ** 6), rng.randint(0, 10 ** 6)
            self.assertEqual(ex.gcd(a, b), math.gcd(a, b))
            self.assertEqual(ex.lcm(a, b), math.lcm(a, b))
            n = rng.randint(1, 5000)
            self.assertEqual(ex.divisors(n), [d for d in range(1, n + 1) if n % d == 0])
            f = ex.factorize(n)
            self.assertEqual(math.prod(p ** e for p, e in f.items()), n)
            self.assertTrue(all(ex.is_prime(p) for p in f))
            self.assertEqual(sol.count_divisors(n), len(ex.divisors(n)))
            self.assertEqual(sol.ugly_number(n), all(p in (2, 3, 5) for p in f))
        self.assertEqual(sol.count_primes(10), 4)
        self.assertEqual(sol.count_primes(0), 0)

    def test_examples(self) -> None:
        self.assertEqual(ex.sieve(30), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
        self.assertEqual(ex.factorize(360), {2: 3, 3: 2, 5: 1})
        self.assertEqual(ex.bus_meeting_time([12, 18, 30]), 180)
        r = ex.race(50000)
        self.assertLess(r["sieve"], r["trial division each"])
        self.assertEqual(sol.gcd_of_strings("ABCABC", "ABC"), "ABC")
        self.assertEqual(sol.gcd_of_strings("LEET", "CODE"), "")


if __name__ == "__main__":
    unittest.main()
