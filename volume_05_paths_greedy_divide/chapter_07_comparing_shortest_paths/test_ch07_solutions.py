import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_correct_rule_never_early(self) -> None:
        for seed in range(30):
            adj, _ = ex.random_map(40, 100, seed)
            places = sorted(adj)
            s, g = places[0], places[-1]
            want = ex.dij.dijkstra(adj, s)[0].get(g, float("inf"))
            self.assertEqual(ex.bidirectional(adj, s, g)[0], want)

    def test_multi_source(self) -> None:
        adj = ex.dij.weighted_adjacency()
        dist, near = sol.multi_source(adj, ["Library", "Harbour"])
        a, b = ex.dij.dijkstra(adj, "Library")[0], ex.dij.dijkstra(adj, "Harbour")[0]
        for v in adj:
            self.assertEqual(dist[v], min(a[v], b[v]))
        self.assertEqual((near["Museum"], near["Market"], dist["Market"]), ("Harbour", "Library", 7))
        self.assertEqual(sol.multi_source(adj, []), ({}, {}))

    def test_naive_trap(self) -> None:
        self.assertEqual(sol.naive_counterexample(), (11, 9))


if __name__ == "__main__":
    unittest.main()
