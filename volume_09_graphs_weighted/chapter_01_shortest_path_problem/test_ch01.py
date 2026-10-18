import math
import random
import unittest

import ch01_examples as ex
import ch01_solutions as sol


def random_wgraph(rng, n, m, lo=1, hi=9):
    g = {v: {} for v in range(n)}
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            g[a][b] = rng.randint(lo, hi)
    return g


class TestShortestBasics(unittest.TestCase):
    def test_relaxation_matches_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            g = random_wgraph(rng, rng.randint(1, 7), rng.randint(0, 15))
            s = rng.randrange(len(g))
            dist = ex.relax_until_stable(g, s)
            for t in g:
                cost, path = ex.brute_force_shortest(g, s, t)
                self.assertEqual(dist[t], cost)
                d2, route = sol.shortest_with_route(g, s, t)
                self.assertEqual(d2, cost)
                if route:
                    self.assertEqual(ex.route_cost(g, route), cost)

    def test_bfs_is_not_enough(self) -> None:
        city = {"Home": {"School": 4, "Park": 1}, "Park": {"School": 2, "Mall": 6}, "School": {"Mall": 1}, "Mall": {}}
        hops = ex.fewest_hops(city, "Home", "Mall")
        self.assertEqual(len(hops), 3)
        self.assertEqual(ex.route_cost(city, hops), 5)
        self.assertEqual(ex.brute_force_shortest(city, "Home", "Mall"), (4, ["Home", "Park", "School", "Mall"]))
        self.assertEqual(ex.route_cost(city, ["Home", "Mall"]), math.inf)
        self.assertEqual(ex.delivery_eta(city, "Home", 2.5)["Mall"], 10.0)

    def test_solutions(self) -> None:
        self.assertEqual(sol.path_from_parents({"a": None, "b": "a", "c": "b"}, "c"), ["a", "b", "c"])
        self.assertGreaterEqual(sol.count_relaxations({"a": {"b": 1}, "b": {}}, "a"), 1)
        self.assertEqual(sol.make_two_way([("A", "B", 3)]), {"A": {"B": 3}, "B": {"A": 3}})


if __name__ == "__main__":
    unittest.main()
