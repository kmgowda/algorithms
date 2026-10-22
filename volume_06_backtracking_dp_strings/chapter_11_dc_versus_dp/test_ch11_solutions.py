import math
import unittest
from collections import Counter

import ch11_examples as ex
import ch11_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_ranges_distinct(self) -> None:
        for n in range(1, 200):
            s = Counter()
            ex.merge_sort_ranges(0, n, s)
            self.assertEqual(ex.summary(s), (2 * n - 1, 2 * n - 1))

    def test_one_row(self) -> None:
        for n in range(0, 30):
            for k in range(-1, n + 2):
                self.assertEqual(sol.choose_one_row(n, k), math.comb(n, k) if 0 <= k <= n else 0)

    def test_k_too_big(self) -> None:
        self.assertEqual(ex.choose(2, 3, Counter()), 0)
        self.assertEqual(ex.choose(3, -1, Counter()), 0)
        self.assertEqual(ex.choose_table(2, 3), (0, 0))


if __name__ == "__main__":
    unittest.main()
