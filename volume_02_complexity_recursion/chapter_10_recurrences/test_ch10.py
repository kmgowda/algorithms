import math
import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestRecurrences(unittest.TestCase):
    def test_closed_forms(self) -> None:
        for n in range(0, 200):
            self.assertEqual(ex.t_shrink_by_one(n), n)
            self.assertEqual(ex.t_hanoi(n % 40), 2 ** (n % 40) - 1)
            self.assertEqual(ex.t_shrink_by_one_linear_work(n), n * (n + 1) // 2)
        for n in range(1, 5000):
            self.assertEqual(ex.t_halving(n), n.bit_length() - 1)
            self.assertEqual(ex.t_two_halves_constant(n), 2 * n - 1)
        for k in range(0, 15):
            self.assertEqual(ex.t_split_and_merge(2 ** k), k * 2 ** k)

    def test_unroll(self) -> None:
        lines = ex.unroll_halving(16)
        self.assertEqual(lines[0], "T(n) = T(n/2) + 1")
        self.assertEqual(lines[-1], "stops after 4 halvings, so T(n) = 4")

    def test_level_work(self) -> None:
        self.assertEqual(ex.level_work(2, 2, 1, 16), [16, 16, 16, 16, 16])
        self.assertEqual(ex.level_work(1, 2, 0, 16), [1, 1, 1, 1, 1])
        self.assertEqual(ex.level_work(4, 2, 1, 4), [4, 8, 16])
        self.assertEqual(ex.level_work(1, 2, 1, 16), [16, 8, 4, 2, 1])

    def test_master(self) -> None:
        self.assertEqual(ex.master_theorem(1, 2, 0), "Theta(log n)")
        self.assertEqual(ex.master_theorem(2, 2, 0), "Theta(n)")
        self.assertEqual(ex.master_theorem(2, 2, 1), "Theta(n log n)")
        self.assertEqual(ex.master_theorem(3, 2, 1), "Theta(n^1.58)")
        self.assertEqual(ex.master_theorem(1, 2, 1), "Theta(n)")
        with self.assertRaises(ValueError):
            ex.master_theorem(2, 1, 1)


class TestDivideAndConquer(unittest.TestCase):
    def test_tournament_and_merge(self) -> None:
        rng = random.Random(10)
        for _ in range(200):
            values = [rng.randint(-100, 100) for _ in range(rng.randint(1, 40))]
            best, comparisons = ex.tournament_max(values)
            self.assertEqual(best, max(values))
            self.assertEqual(comparisons, len(values) - 1)
            ordered, work = ex.merge_sort_counting(values)
            self.assertEqual(ordered, sorted(values))
        self.assertEqual(ex.merge_sort_counting(list(range(16)))[1], 16 * 4)

    def test_word_count(self) -> None:
        counts, depth = ex.word_count_split(["the lion", "the zebra", "a lion", "the end"])
        self.assertEqual(counts, {"the": 3, "lion": 2, "zebra": 1, "a": 1, "end": 1})
        self.assertEqual(depth, 2)
        self.assertEqual(ex.word_count_split([]), ({}, 0))


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertEqual(sol.exercise1_answers()["T(n) = 2T(n/2) + n"], "Theta(n log n)")
        answers = sol.exercise2_master()
        self.assertEqual(answers["T(n) = 4T(n/2) + n^2"], "Theta(n^2 log n)")
        self.assertEqual(answers["T(n) = 8T(n/2) + n^2"], "Theta(n^3)")
        self.assertEqual(answers["T(n) = 2T(n/2) + n^2"], "Theta(n^2)")
        self.assertEqual(answers["T(n) = 9T(n/3) + n"], "Theta(n^2)")
        self.assertEqual(sol.t_power_two_calls(1024), 2047)
        self.assertEqual(sol.t_ternary_search(3 ** 10), 20)
        self.assertAlmostEqual(sol.fibonacci_calls_ratio(30), (1 + math.sqrt(5)) / 2, places=5)


if __name__ == "__main__":
    unittest.main()
