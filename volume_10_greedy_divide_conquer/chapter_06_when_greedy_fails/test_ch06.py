import itertools
import random
import unittest

import ch06_examples as ex
import ch06_solutions as sol


class TestGreedyFails(unittest.TestCase):
    def test_knapsack(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            items = [(f"i{k}", rng.randint(1, 6), rng.randint(1, 20)) for k in range(rng.randint(0, 5))]
            cap = rng.randint(0, 12)
            brute = max((sum(v for _, _, v in c) for r in range(len(items) + 1)
                         for c in itertools.combinations(items, r) if sum(w for _, w, _ in c) <= cap), default=0)
            best = ex.knapsack_best(items, cap)
            self.assertEqual(best, brute)
            self.assertLessEqual(ex.knapsack_greedy(items, cap), best)
            self.assertGreaterEqual(2 * sol.best_of_two_knapsack(items, cap), best)
        self.assertEqual((ex.knapsack_greedy([("camera", 5, 60), ("laptop", 4, 40), ("books", 4, 40)], 8),
                          ex.knapsack_best([("camera", 5, 60), ("laptop", 4, 40), ("books", 4, 40)], 8)), (60, 80))

    def test_tsp_and_cover(self) -> None:
        towns = [(0, 0), (1, 0), (-2, 0), (4, 0), (-8, 0)]   # zigzag along a road
        self.assertGreater(ex.nearest_neighbour_tour(towns), ex.best_tour(towns))
        rng = random.Random(2)
        for _ in range(30):
            pts = [(rng.random(), rng.random()) for _ in range(rng.randint(2, 6))]
            self.assertGreaterEqual(ex.nearest_neighbour_tour(pts) + 1e-9, ex.best_tour(pts))
        cover = {"A": {"1", "2", "3", "4"}, "B": {"1", "2", "5"}, "C": {"3", "4", "6"}}
        u = {"1", "2", "3", "4", "5", "6"}
        self.assertEqual(len(ex.greedy_set_cover(u, cover)), 3)
        self.assertEqual(ex.smallest_cover(u, cover), 2)
        with self.assertRaises(ValueError):
            ex.greedy_set_cover({"x"}, {"A": {"y"}})

    def test_rules_and_solutions(self) -> None:
        r = ex.wrong_activity_rules()
        self.assertLess(r["earliest start"], r["earliest end (correct)"])
        self.assertLess(r["shortest first"], r["earliest end on the same input"])
        found = sol.find_knapsack_counterexample()
        self.assertIsNotNone(found)
        self.assertLess(found[2], found[3])
        self.assertEqual(sol.coin_counterexample([1, 3, 4]), 6)
        self.assertIsNone(sol.coin_counterexample([1, 5, 10, 25]))
        self.assertEqual(sol.coin_counterexample([1, 7, 10]), 14)


if __name__ == "__main__":
    unittest.main()
