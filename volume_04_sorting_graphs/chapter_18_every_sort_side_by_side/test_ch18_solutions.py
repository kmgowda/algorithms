import math
import random
import unittest

import ch18_examples as ex
import ch18_solutions as sol


class TestChapter15Thinking(unittest.TestCase):
    def test_depth_lower_bound(self) -> None:
        """Thinking Problem 15.1: after d stages a wire is reached by at most 2^d inputs."""
        for n in range(1, 17):
            net = ex.sorting_network(n)
            depth = len(ex.stages(net))
            reach = sol.influence_sets(net, n)
            self.assertTrue(all(len(r) <= 2 ** depth for r in reach))
            self.assertEqual(len(reach[0]), n)
            self.assertGreaterEqual(depth, math.ceil(math.log2(n)) if n > 1 else 0)
        self.assertEqual(sol.influence_sets([], 1), [{0}])

    def test_sort_k_sorted(self) -> None:
        self.assertEqual(sol.sort_k_sorted([], 3), [])
        self.assertEqual(sol.sort_k_sorted([47], 0), [47])
        self.assertEqual(sol.sort_k_sorted([12, 25, 31], 0), [12, 25, 31])
        self.assertEqual(sol.sort_k_sorted([25, 12, 58, 31, 47, 70, 63, 91, 84], 2),
                         [12, 25, 31, 47, 58, 63, 70, 84, 91])
        self.assertEqual(sol.sort_k_sorted(ex.PILE, 100), sorted(ex.PILE))
        rng = random.Random(6)
        for _ in range(300):
            n, k = rng.randint(0, 40), rng.randint(0, 6)
            a = sorted(rng.randint(0, 50) for _ in range(n))
            for i in range(0, n - 1):            # local swaps keep every item within k places
                if rng.random() < 0.5:
                    j = min(n - 1, i + rng.randint(0, k))
                    a[i], a[j] = a[j], a[i]
            srt = sorted(a)
            if all(any(srt[p] == x for p in range(max(0, i - k), min(n, i + k + 1))) for i, x in enumerate(a)):
                self.assertEqual(sol.sort_k_sorted(a, k), srt)

    def test_odd_even_transposition(self) -> None:
        self.assertEqual(sol.odd_even_transposition(1, 3), [])
        self.assertEqual(sol.odd_even_transposition(2, 1), [(0, 1)])
        net7 = sol.odd_even_transposition(8, 7)
        self.assertEqual(len(net7), 25)
        self.assertEqual(sol.first_01_failure(net7, 8), [1, 1, 0, 0, 0, 0, 0, 0])
        self.assertEqual(ex.apply_network(net7, [84, 91, 12, 25, 31, 47, 58, 63]), [12, 25, 31, 47, 58, 84, 63, 91])
        for n in range(1, 10):
            self.assertIsNone(sol.first_01_failure(sol.odd_even_transposition(n, n), n))
            if n > 2:
                self.assertIsNotNone(sol.first_01_failure(sol.odd_even_transposition(n, n - 1), n))


if __name__ == "__main__":
    unittest.main()
