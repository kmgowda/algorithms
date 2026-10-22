import unittest

import ch22_examples as ex


class TestChapter62(unittest.TestCase):
    def test_every_case(self) -> None:
        v = ["A", "B", "C"]
        self.assertEqual((ex.adjacency_matrix([], []), ex.adjacency_list([], [])), ([], {}))
        self.assertEqual(ex.degrees(ex.adjacency_list(v, [])), {"A": 0, "B": 0, "C": 0})
        self.assertEqual(ex.adjacency_matrix(v, [("A", "A")])[0][0], 1)
        self.assertEqual(ex.degrees(ex.adjacency_list(v, [("A", "A")]))["A"], 2)
        twice = [("A", "B"), ("A", "B")]
        self.assertEqual((ex.adjacency_matrix(v, twice)[0], ex.adjacency_list(v, twice)["A"]), ([0, 1, 0], ["B", "B"]))
        for build in (ex.adjacency_matrix, ex.adjacency_list):
            with self.assertRaises(KeyError):
                build(v, [("A", "Z")])
        self.assertEqual(ex.weighted_adjacency([("A", "B", 5), ("A", "B", 3)]), {"A": {"B": 3}, "B": {}})
        g = ["...", ".#.", "..."]
        self.assertEqual((ex.grid_neighbours(g, 0, 0), ex.grid_neighbours(g, 1, 0), ex.grid_neighbours(["."], 0, 0)),
                         ([(1, 0), (0, 1)], [(0, 0), (2, 0)], []))

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

    def test_compressed(self) -> None:
        start, targets = ex.compressed(ex.BRANCHES, ex.ROUTES)
        self.assertEqual(start, [0, 4, 6, 8, 10, 12, 14])
        self.assertEqual(targets[:4], ["North", "East", "South", "West"])
        adj = ex.adjacency_list(ex.BRANCHES, ex.ROUTES)
        for v in ex.BRANCHES:
            self.assertEqual(ex.compressed_neighbours(ex.BRANCHES, start, targets, v), adj[v])
        self.assertEqual(ex.compressed([], []), ([0], []))
        self.assertEqual(ex.compressed(["A", "B"], []), ([0, 0, 0], []))

    def test_experiment_sizes(self) -> None:
        out = ex.experiment(n=200, m=500, queries=200)
        self.assertEqual((out["matrix cells"], out["list entries"]), (40000, 1000))


if __name__ == "__main__":
    unittest.main()
