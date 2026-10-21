import unittest

import ch62_examples as ex


class TestChapter62(unittest.TestCase):
    def test_courier_map(self) -> None:
        m = ex.adjacency_matrix(ex.BRANCHES, ex.ROUTES)
        adj = ex.adjacency_list(ex.BRANCHES, ex.ROUTES)
        self.assertEqual(m[0], [0, 1, 1, 1, 1, 0])
        self.assertEqual(m[5], [0, 0, 0, 1, 1, 0])
        self.assertEqual(sum(map(sum, m)), 2 * len(ex.ROUTES))
        self.assertEqual(sum(ex.degrees(adj).values()), 2 * len(ex.ROUTES))
        for i, a in enumerate(ex.BRANCHES):
            for j, b in enumerate(ex.BRANCHES):
                self.assertEqual(m[i][j] == 1, b in adj[a])

    def test_directed_weighted_and_grid(self) -> None:
        w = ex.weighted_adjacency([("A", "B", 5), ("B", "C", 2), ("C", "A", 7)])
        self.assertEqual(w, {"A": {"B": 5}, "B": {"C": 2}, "C": {"A": 7}})
        grid = ["..#", ".#.", "..."]
        self.assertEqual(sorted(ex.grid_neighbours(grid, 0, 0)), [(0, 1), (1, 0)])
        self.assertEqual(ex.grid_neighbours(grid, 1, 2), [(2, 2)])

    def test_experiment_sizes(self) -> None:
        out = ex.experiment(n=200, m=500, queries=200)
        self.assertEqual((out["matrix cells"], out["list entries"]), (40000, 1000))


if __name__ == "__main__":
    unittest.main()
