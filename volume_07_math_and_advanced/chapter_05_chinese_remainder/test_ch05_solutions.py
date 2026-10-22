import math
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual(sol.mixed_radix_digits([], []), [])
        self.assertEqual(sol.rebuilt_mod([], [], 7), 0)
        self.assertEqual(sol.rebuilt_mod([5], [7], 1), 0)
        self.assertEqual(sol.rebuilt_mod([0], [1], 5), 0)
        self.assertEqual(sol.rebuilt_mod([12], [7], 100), 5)

    def test_sunzi(self) -> None:
        self.assertEqual(sol.mixed_radix_digits([2, 3, 2], [3, 5, 7]), [2, 2, 1])
        self.assertEqual(sol.rebuilt_mod([2, 3, 2], [3, 5, 7], 4), 3)

    def test_against_full_rebuild(self) -> None:
        rng = random.Random(5)
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 97, 101]
        for _ in range(300):
            ms = rng.sample(primes, rng.randint(1, 5))
            rs = [rng.randint(0, 200) for _ in ms]
            q = rng.randint(1, 1000)
            x, _ = ex.crt(rs, ms)
            self.assertEqual(sol.rebuilt_mod(rs, ms, q), x % q)
            d = sol.mixed_radix_digits(rs, ms)
            self.assertTrue(all(0 <= di < m for di, m in zip(d, ms)))

    def test_square_roots_of_one(self) -> None:
        self.assertEqual(sol.square_roots_of_one(15), [1, 4, 11, 14])
        self.assertEqual(len(sol.square_roots_of_one(105)), 8)
        self.assertEqual(sol.square_roots_of_one(7), [1, 6])
        self.assertEqual(sol.square_roots_of_one(1), [0])

    def test_setwise_coprime_is_not_enough(self) -> None:
        self.assertTrue(sol.unique_if_setwise_coprime([6, 10, 15]))
        self.assertEqual(ex.crt([0, 1, 0], [6, 10, 15])[0], None)
        hits = [x for x in range(900) if x % 6 == 0 and x % 10 == 0 and x % 15 == 0]
        self.assertEqual(len(hits), 30)


if __name__ == "__main__":
    unittest.main()
