import unittest

import ch11_examples as ex
import ch11_solutions as sol


class TestComparison(unittest.TestCase):
    def test_orders(self) -> None:
        adj = ex.to_list(8, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (6, 7)])
        self.assertEqual(ex.bfs_order(adj, 0), [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(sorted(ex.dfs_order(adj, 0)), list(range(8)))
        mat = ex.to_matrix(8, [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (6, 7)])
        self.assertEqual(ex.bfs_matrix(mat, 0), ex.bfs_order(adj, 0))

    def test_frontiers(self) -> None:
        star = ex.to_list(101, [(0, i) for i in range(1, 101)])
        chain = ex.to_list(101, [(i, i + 1) for i in range(100)])
        self.assertEqual(ex.peak_frontier(star, 0), {"DFS stack": 2, "BFS queue": 100})
        self.assertEqual(ex.peak_frontier(chain, 0), {"DFS stack": 101, "BFS queue": 1})

    def test_races(self) -> None:
        r = ex.race_representations(800, 2000)
        self.assertLess(r["BFS on adjacency list"], r["BFS on matrix"])
        answers, _, _ = ex.connectivity_queries(500, ex.random_edges(500, 400, 2), [(i, i * 7 % 500) for i in range(500)])
        self.assertEqual(len(answers), 500)

    def test_solutions(self) -> None:
        picks = sol.pick_for_scenarios()
        self.assertEqual(picks["fewest train changes between two stations"], "BFS")
        self.assertEqual(picks["friend groups as a social network grows"], "union-find")
        self.assertEqual(sol.frontier_shapes()["long, thin (a chain)"], "BFS")


if __name__ == "__main__":
    unittest.main()
