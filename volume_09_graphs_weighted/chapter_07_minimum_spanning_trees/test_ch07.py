import itertools
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


class TestMST(unittest.TestCase):
    def test_random_connected(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            n = rng.randint(1, 6)
            vertices = list(range(n))
            edges = [(rng.randint(1, 9), i, rng.randrange(i)) for i in range(1, n)]       # a spanning tree
            for _ in range(rng.randint(0, 6)):
                a, b = rng.sample(range(n), 2) if n > 1 else (0, 0)
                if a != b:
                    edges.append((rng.randint(1, 9), a, b))
            k_total, k_edges = ex.kruskal(vertices, edges)
            g = {v: {} for v in vertices}
            for w, u, v in edges:
                if v not in g[u] or w < g[u][v]:
                    g[u][v] = g[v][u] = w
            p_total, p_edges = ex.prim(g, 0)
            self.assertEqual(k_total, sol.brute_force_mst(vertices, edges))
            self.assertEqual(p_total, k_total)
            self.assertEqual(len(k_edges), n - 1)
            self.assertEqual(len(p_edges), n - 1)

    def test_examples(self) -> None:
        towns = ["A", "B", "C", "D", "E"]
        cables = [(4, "A", "B"), (1, "A", "C"), (3, "B", "C"), (2, "B", "D"), (5, "C", "D"), (7, "D", "E"), (6, "C", "E")]
        self.assertEqual(ex.kruskal(towns, cables)[0], 12)
        pts = [(0, 0), (2, 2), (3, 10), (5, 2), (7, 0)]
        self.assertEqual(ex.connect_points(pts), 20)
        edges = [(abs(a[0] - b[0]) + abs(a[1] - b[1]), i, j) for (i, a), (j, b) in itertools.combinations(enumerate(pts), 2)]
        self.assertEqual(ex.kruskal(list(range(5)), edges)[0], 20)
        self.assertEqual(ex.clusters({"lion": (0, 0), "tiger": (1, 0), "zebra": (10, 10), "horse": (11, 10), "eagle": (5, 20)}, 3),
                         [["eagle"], ["horse", "zebra"], ["lion", "tiger"]])

    def test_solutions(self) -> None:
        towns = ["A", "B", "C", "D", "E"]
        cables = [(4, "A", "B"), (1, "A", "C"), (3, "B", "C"), (2, "B", "D"), (5, "C", "D"), (7, "D", "E"), (6, "C", "E")]
        self.assertEqual(sol.maximum_spanning_tree(towns, cables), 20)   # 7 + 6 + 4 + 3; edge 5 would close a loop
        self.assertEqual(sol.min_cost_with_wells(3, [1, 2, 2], [(1, 2, 1), (2, 3, 1)]), 3)
        self.assertTrue(sol.is_unique_mst(towns, cables))
        self.assertFalse(sol.is_unique_mst(["a", "b", "c"], [(1, "a", "b"), (1, "b", "c"), (1, "a", "c")]))


if __name__ == "__main__":
    unittest.main()
