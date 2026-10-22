import itertools
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol


def all_walks(out, v, goal, cost=0):
    if v == goal:
        yield cost
    for b, w in out[v]:
        yield from all_walks(out, b, goal, cost + w)


class TestChapter4Solutions(unittest.TestCase):
    def test_trail(self) -> None:
        dist, ways = sol.count_quickest_walks(ex.STOPS, ex.PATHS, "Gate")
        self.assertEqual((dist["Stage"], ways["Stage"]), (7, 1))
        closed = [p for p in ex.PATHS if p[2] != -2]
        dist, ways = sol.count_quickest_walks(ex.STOPS, closed, "Gate")
        self.assertEqual((dist["Stage"], ways["Stage"]), (13, 2))

    def test_smallest(self) -> None:
        self.assertEqual(sol.count_quickest_walks(["A"], [], "A"), ({"A": 0}, {"A": 1}))
        d, w = sol.count_quickest_walks(["A", "B"], [], "A")
        self.assertEqual((d["B"], w["B"]), (float("inf"), 0))
        with self.assertRaises(ValueError):
            sol.count_quickest_walks(["A", "B"], [("A", "B", 1), ("B", "A", 1)], "A")

    def test_random_dags(self) -> None:
        rng = random.Random(4)
        for _ in range(200):
            n = rng.randint(1, 6)
            edges = [(a, b, rng.randint(-2, 3)) for a, b in itertools.combinations(range(n), 2) if rng.random() < 0.5]
            out = {v: [] for v in range(n)}
            for a, b, w in edges:
                out[a].append((b, w))
            dist, ways = sol.count_quickest_walks(list(range(n)), edges, 0)
            for t in range(n):
                costs = list(all_walks(out, 0, t))
                best = min(costs, default=float("inf"))
                self.assertEqual((dist[t], ways[t]), (best, costs.count(best) if costs else 0))

    def test_backward_pass_order_bug(self) -> None:
        wrong = sol.latest_in_forward_order(ex.BUILD, ex.BEFORE)
        right = ex.critical_path(ex.BUILD, ex.BEFORE)[2]
        self.assertEqual((wrong["frame"], right["frame"]), (2, 0))


if __name__ == "__main__":
    unittest.main()
