import math
import unittest

import ch01_examples as ex
import ch01_solutions as sol


class TestMeasuredThings(unittest.TestCase):
    def test_search_and_pairs(self) -> None:
        self.assertEqual(ex.find_book_linear([5, 7, 9], 9), 2)
        self.assertEqual(ex.find_book_linear([], 9), -1)
        self.assertEqual(ex.count_matching_pairs([1, 2, 1, 1]), 3)
        self.assertEqual(ex.count_matching_pairs([]), 0)

    def test_step_counts(self) -> None:
        self.assertEqual(ex.linear_steps(1000), 1000)
        self.assertEqual(ex.pair_steps(10), 45)
        self.assertEqual(ex.halving_steps(1024), 10)

    def test_doubling_ratios_identify_growth(self) -> None:
        sizes = [1000, 2000, 4000, 8000]
        for ratio in ex.doubling_ratios(ex.linear_steps, sizes):
            self.assertAlmostEqual(ratio, 2.0)
        for ratio in ex.doubling_ratios(ex.pair_steps, sizes):
            self.assertAlmostEqual(ratio, 4.0, delta=0.01)
        for ratio in ex.doubling_ratios(ex.halving_steps, sizes):
            self.assertLess(ratio, 1.2)

    def test_exponent(self) -> None:
        self.assertAlmostEqual(ex.estimated_exponent(2), 1)
        self.assertAlmostEqual(ex.estimated_exponent(8), 3)

    def test_timers_return_positive_seconds(self) -> None:
        self.assertGreater(ex.best_time(lambda: sum(range(1000)), repeats=2), 0)
        self.assertGreater(ex.timeit_seconds(lambda: sum(range(100)), number=10, repeat=2), 0)
        self.assertGreater(ex.timed_cost(sum)(1000), 0)


class TestSolutions(unittest.TestCase):
    def test_predict(self) -> None:
        self.assertAlmostEqual(sol.predict_time(2.0, 10_000, 1_000_000, 2), 20_000.0)
        self.assertAlmostEqual(sol.predict_time(2.0, 10_000, 1_000_000, 1), 200.0)

    def test_triple(self) -> None:
        for n in range(0, 15):
            self.assertEqual(sol.triple_loop_steps(n), math.comb(n, 3))
        ratio = sol.triple_loop_steps(200) / sol.triple_loop_steps(100)
        self.assertEqual(sol.classify_ratio(ratio), "cubic or worse")

    def test_classify(self) -> None:
        self.assertEqual(sol.classify_ratio(1.05), "constant or logarithmic")
        self.assertEqual(sol.classify_ratio(2.1), "linear (or n log n)")
        self.assertEqual(sol.classify_ratio(3.9), "quadratic")
        self.assertEqual(sol.steps_for_report(500, 6), 3000)


if __name__ == "__main__":
    unittest.main()
