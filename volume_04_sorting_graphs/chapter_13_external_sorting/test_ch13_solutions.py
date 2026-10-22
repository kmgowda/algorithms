import math
import random
import unittest

import ch13_examples as ex
import ch13_solutions as sol


class TestChapter13Thinking(unittest.TestCase):
    def test_cheapest_merge_order_small(self) -> None:
        self.assertEqual(sol.cheapest_merge_order([]), (0, []))
        self.assertEqual(sol.cheapest_merge_order([7]), (0, []))
        self.assertEqual(sol.cheapest_merge_order([3, 4]), (7, [(3, 4)]))
        self.assertEqual(sol.cheapest_merge_order([5, 5, 5]), (25, [(5, 5), (5, 10)]))

    def test_cheapest_merge_order_example(self) -> None:
        runs = [20, 30, 10, 5, 30]
        self.assertEqual(sol.cheapest_merge_order(runs), (205, [(5, 10), (15, 20), (30, 30), (35, 60)]))
        self.assertEqual(sol.merge_cost_in_order(runs), 270)
        self.assertEqual(sol.cheapest_by_brute_force(runs), 205)

    def test_cheapest_merge_order_is_optimal(self) -> None:
        rng = random.Random(4)
        for _ in range(150):
            runs = [rng.randint(1, 40) for _ in range(rng.randint(0, 6))]
            self.assertEqual(sol.cheapest_merge_order(runs)[0], sol.cheapest_by_brute_force(runs))

    def test_replacement_selection_never_more_runs(self) -> None:
        """Thinking Problem 13.1: every run but the last has at least M items, so at most ceil(n / M) runs."""
        rng = random.Random(2)
        for _ in range(2000):
            n, m = rng.randint(0, 80), rng.randint(1, 10)
            a = [rng.randint(0, 30) for _ in range(n)]
            runs = ex.replacement_selection(a, m)
            self.assertLessEqual(len(runs), math.ceil(n / m))
            self.assertTrue(all(len(r) >= m for r in runs[:-1]))
        self.assertEqual([len(r) for r in ex.replacement_selection(list(range(20, 0, -1)), 4)], [4] * 5)

    def test_polyphase_needs_a_fibonacci_split(self) -> None:
        """Thinking Problem 13.3: other splits of 13 runs take more phases and copy more."""
        for a, b, phases, written in [(8, 5, 5, 50), (7, 6, 7, 60), (12, 1, 12, 90)]:
            log = ex.polyphase(a, b)
            self.assertEqual((len(log), sum(w for _, w in log)), (phases, written))
        self.assertEqual(ex.polyphase(7, 6)[:2], [((1, 0, 6), 12), ((0, 1, 5), 3)])
        with self.assertRaises(ValueError):
            ex.polyphase(13, 0)
        with self.assertRaises(ValueError):
            ex.polyphase(0, 2)
        self.assertEqual(ex.polyphase(0, 1), [])
        self.assertEqual(ex.polyphase(0, 0), [])


if __name__ == "__main__":
    unittest.main()
