import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_smallest_inputs(self) -> None:
        self.assertEqual([sol.split_by_square_root(n, [2]) for n in (0, 1, 2, 3)], [None] * 4)
        self.assertEqual(sol.split_by_square_root(4, [3]), 2)
        self.assertIsNone(sol.split_by_square_root(561, []))
        self.assertEqual(sol.split_by_square_root(9, [3]), 3)              # the base shares a factor

    def test_splits_carmichael_numbers(self) -> None:
        self.assertEqual(sol.split_by_square_root(561, [2]), 33)
        for n in (561, 1105, 1729, 2465, 2821, 6601, 8911):
            d = sol.split_by_square_root(n, [2, 3, 5, 7, 11])
            self.assertTrue(d is not None and 1 < d < n and n % d == 0)

    def test_primes_are_never_split(self) -> None:
        for p in (5, 7, 97, 7919, 2 ** 61 - 1):
            self.assertIsNone(sol.split_by_square_root(p, [2, 3, 5, 7]))

    def test_any_factor_found_is_proper(self) -> None:
        for n in range(5, 3000, 2):
            d = sol.split_by_square_root(n, [2, 3, 5])
            if d is not None:
                self.assertTrue(1 < d < n and n % d == 0)

    def test_strong_liars_not_closed(self) -> None:
        self.assertEqual(sol.strong_liars(65), [1, 8, 18, 47, 57, 64])
        self.assertFalse(ex.is_strong_liar(65, 8 * 18 % 65))
        self.assertEqual(ex.squaring_chain(65, 14)[:2], [14, 1])

    def test_last_step_only_is_fooled(self) -> None:
        self.assertTrue(sol.last_step_only(561, 2))
        self.assertFalse(ex.is_strong_liar(561, 2))


if __name__ == "__main__":
    unittest.main()
