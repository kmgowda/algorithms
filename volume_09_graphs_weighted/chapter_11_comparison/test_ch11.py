import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestComparison(unittest.TestCase):
    def test_algorithms_agree(self) -> None:
        for seed in range(5):
            adj, edges = ex.random_road_grid(6, seed)
            V = 36
            fw = ex.floyd_warshall(V, edges)
            for s in (0, 7, 35):
                d = ex.dijkstra(adj, s)
                self.assertEqual(d, ex.bellman_ford(V, edges, s))
                self.assertEqual(d, fw[s])
            cost, expanded = ex.a_star(adj, 6, 0, 35)
            self.assertEqual(cost, ex.dijkstra(adj, 0)[35])
            self.assertLessEqual(expanded, V)

    def test_race(self) -> None:
        r = ex.race_shortest(8)
        self.assertLess(r["Dijkstra"], r["Bellman-Ford"])

    def test_solutions(self) -> None:
        picks = sol.pick_for_scenarios()
        self.assertEqual(picks["phone navigation to one address"], "A*")
        self.assertEqual(picks["a project's earliest finish time"], "DAG relaxation in topological order")
        t = sol.mst_vs_shortest_path_tree()
        self.assertLess(t["MST total"], t["shortest-path tree total"])
        self.assertLess(t["A to C shortest"], t["A to C in MST"])


if __name__ == "__main__":
    unittest.main()
