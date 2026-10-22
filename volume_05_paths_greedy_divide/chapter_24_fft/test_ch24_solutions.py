import random
import unittest
from collections import Counter

import ch24_examples as ex
import ch24_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_halving_lemma(self) -> None:
        for n in (1, 2, 4, 8, 16, 64):
            self.assertTrue(sol.squared_roots_match(n))

    def test_pair_sums(self) -> None:
        self.assertEqual(sol.pair_sum_counts([3, 5, 5, 8], [2, 4, 7]), {5: 1, 7: 3, 9: 2, 10: 2, 12: 3, 15: 1})
        self.assertEqual(sol.pair_sum_counts([], [1]), {})
        r = random.Random(24)
        for _ in range(100):
            a = [r.randint(0, 20) for _ in range(r.randint(1, 15))]
            b = [r.randint(0, 20) for _ in range(r.randint(1, 15))]
            self.assertEqual(sol.pair_sum_counts(a, b), dict(Counter(x + y for x in a for y in b)))

    def test_unpadded(self) -> None:
        self.assertEqual(sol.unpadded_square([1, 1, 1, 1]), [4, 4, 4, 4])
        self.assertEqual(ex.fft_multiply([1, 1, 1, 1], [1, 1, 1, 1]), [1, 2, 3, 4, 3, 2, 1])


if __name__ == "__main__":
    unittest.main()
