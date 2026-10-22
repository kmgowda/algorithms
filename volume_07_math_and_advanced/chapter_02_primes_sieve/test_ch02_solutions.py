import unittest

import ch02_examples as ex
import ch02_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.distinct_prime_counts(0), [0])
        self.assertEqual(sol.distinct_prime_counts(1), [0, 0])
        self.assertEqual(sol.distinct_prime_counts(2), [0, 0, 1])

    def test_against_factorise(self) -> None:
        omega = sol.distinct_prime_counts(5000)
        for m in range(1, 5001):
            self.assertEqual(omega[m], len(set(ex.factorise(m))))
        self.assertEqual((omega[360], omega[2310]), (3, 5))

    def test_buggy_window_loses_small_primes(self) -> None:
        self.assertEqual(sol.segmented_sieve_buggy(2, 20), [5, 7, 11, 13, 17, 19])
        self.assertEqual(ex.segmented_sieve(2, 20), [2, 3, 5, 7, 11, 13, 17, 19])
        self.assertEqual(sol.segmented_sieve_buggy(90, 100), ex.segmented_sieve(90, 100))

    def test_composite_run(self) -> None:
        for n in range(1, 8):
            run = sol.composite_run(n)
            self.assertEqual(len(run), n)
            for k, x in enumerate(run, start=2):
                self.assertEqual(x % k, 0)


class TestAgreement(unittest.TestCase):
    def test_three_methods_agree_to_10000(self) -> None:
        primes = set(ex.sieve(10_000)[0])
        spf, _ = ex.smallest_factor_sieve(10_000)
        for n in range(2, 10_001):
            self.assertEqual(ex.is_prime(n)[0], n in primes)
            self.assertEqual(spf[n] == n, n in primes)


if __name__ == "__main__":
    unittest.main()
