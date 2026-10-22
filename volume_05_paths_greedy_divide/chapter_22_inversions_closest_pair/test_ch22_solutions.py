import random
import unittest

import ch22_examples as ex
import ch22_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_swaps_equal_inversions(self) -> None:
        r = random.Random(22)
        for _ in range(200):
            a = [r.randint(0, 9) for _ in range(r.randint(0, 12))]
            self.assertEqual(sol.neighbour_swaps(a), ex.inversions_brute(a))
        self.assertEqual(sol.neighbour_swaps(ex.RANKS), 9)

    def test_gap_pairs(self) -> None:
        r = random.Random(3)
        for _ in range(200):
            a = [r.randint(0, 20) for _ in range(r.randint(0, 14))]
            k = r.randint(0, 6)
            want = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] - a[j] > k)
            self.assertEqual(sol.gap_pairs(a, k), want)
        self.assertEqual(sol.gap_pairs(ex.RANKS, 0), 9)

    def test_strict_bug(self) -> None:
        self.assertEqual((sol.sort_count_strict([2, 2]), ex.sort_count([2, 2])[1]), (1, 0))
        self.assertEqual(sol.sort_count_strict(ex.RANKS), 9)


if __name__ == "__main__":
    unittest.main()
