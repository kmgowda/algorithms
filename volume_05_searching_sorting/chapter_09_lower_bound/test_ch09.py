import itertools
import math
import random
import unittest

import ch09_examples as ex
import ch09_solutions as sol


class TestLowerBound(unittest.TestCase):
    def test_bound_values(self) -> None:
        self.assertEqual([ex.lower_bound_comparisons(n) for n in range(1, 8)], [0, 1, 3, 5, 7, 10, 13])
        for n in (10, 100, 1000):
            self.assertLess(abs(ex.stirling_estimate(n) - math.log2(math.factorial(n))), 2 * math.log2(n) + 2)

    def test_no_sort_beats_the_bound(self) -> None:
        for n in range(2, 7):
            self.assertGreaterEqual(ex.worst_case_comparisons(sorted, n), ex.lower_bound_comparisons(n))

    def test_counted(self) -> None:
        self.assertEqual(ex.comparisons_used(sorted, [1, 2]), 1)

    def test_sort_three_is_optimal(self) -> None:
        for p in itertools.permutations([1, 2, 3]):
            self.assertEqual(ex.sort_three(*p), (1, 2, 3))
            ex.Counted.comparisons = 0
            ex.sort_three(*(ex.Counted(v) for v in p))
            self.assertLessEqual(ex.Counted.comparisons, 3)

    def test_guessing(self) -> None:
        self.assertEqual(ex.guessing_game_questions(1_000_000), 20)
        self.assertEqual(ex.guessing_game_questions(1), 0)


class TestSolutions(unittest.TestCase):
    def test_min_max(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            v = [rng.randint(-50, 50) for _ in range(rng.randint(1, 20))]
            lo, hi, comps = sol.min_and_max(v)
            self.assertEqual((lo, hi), (min(v), max(v)))
            self.assertLessEqual(comps, math.ceil(3 * len(v) / 2))
        with self.assertRaises(ValueError):
            sol.min_and_max([])

    def test_others(self) -> None:
        self.assertEqual(sol.tournament_rounds_to_rank(8), 16)
        self.assertEqual(sol.weighings_for_fake_coin(9), 2)
        self.assertEqual(sol.weighings_for_fake_coin(10), 3)


if __name__ == "__main__":
    unittest.main()
