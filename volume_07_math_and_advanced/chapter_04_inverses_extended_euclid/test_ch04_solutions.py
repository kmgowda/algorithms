import itertools
import math
import random
import unittest

import ch04_solutions as sol


def brute_keys(n1, c1, n2, c2, m):
    return [(k, s) for k, s in itertools.product(range(m), repeat=2)
            if math.gcd(k, m) == 1 and (k * n1 + s) % m == c1 % m and (k * n2 + s) % m == c2 % m]


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.affine_keys(0, 0, 0, 0, 1), [(0, 0)])            # one letter, one key
        self.assertEqual(sol.affine_keys(5, 9, 5, 10), [])                     # one letter cannot map to two
        self.assertEqual(len(sol.affine_keys(5, 9, 5, 9)), 12)                 # no information: phi(26) keys

    def test_newsletter(self) -> None:
        self.assertEqual(sol.affine_keys(2, 17, 4, 5), [(7, 3)])               # C -> R, E -> F
        self.assertEqual(len(sol.affine_keys(0, 3, 13, 16)), 12)                # A -> D, N -> Q: 13 divides 26

    def test_against_brute_force(self) -> None:
        rng = random.Random(4)
        for _ in range(300):
            m = rng.randint(1, 30)
            n1, n2, c1, c2 = (rng.randrange(m) for _ in range(4))
            self.assertEqual(sol.affine_keys(n1, c1, n2, c2, m), brute_keys(n1, c1, n2, c2, m))

    def test_fermat_fails_for_composites(self) -> None:
        self.assertEqual(sol.inverse_by_fermat_anyway(7, 26), 1)
        self.assertEqual(pow(7, 11, 26), 15)                                    # a^(phi(m) - 1) is right

    def test_wilson(self) -> None:
        primes = [n for n in range(2, 200) if all(n % d for d in range(2, math.isqrt(n) + 1))]
        self.assertEqual([n for n in range(2, 200) if sol.wilson_holds(n)], primes)


if __name__ == "__main__":
    unittest.main()
