import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


class TestRepresentations(unittest.TestCase):
    def test_conversions_agree(self) -> None:
        rng = random.Random(1)
        for _ in range(100):
            n = rng.randint(1, 12)
            edges = sorted({tuple(sorted((rng.randrange(n), rng.randrange(n)))) for _ in range(rng.randint(0, 20))})
            edges = [e for e in edges if e[0] != e[1]]
            adj = ex.edge_list_to_adjacency_list(n, edges)
            mat = ex.edge_list_to_matrix(n, edges)
            self.assertEqual(ex.matrix_to_edge_list(mat), edges)
            self.assertEqual([sorted(r) for r in sol.matrix_to_list(mat)], [sorted(r) for r in adj])
            for u in range(n):
                for v in range(n):
                    self.assertEqual(ex.has_edge_matrix(mat, u, v), ex.has_edge_list(adj, u, v))

    def test_reverse(self) -> None:
        adj = ex.edge_list_to_adjacency_list(3, [(0, 1), (0, 2), (1, 2)], directed=True)
        self.assertEqual(sol.reverse_graph(adj), [[], [0], [0, 1]])
        self.assertEqual(sol.reverse_graph(sol.reverse_graph(adj)), adj)

    def test_labeled_and_memory(self) -> None:
        self.assertEqual(ex.flights_from([("BLR", "DEL"), ("BLR", "BOM"), ("DEL", "BLR")], "BLR"), ["BOM", "DEL"])
        self.assertEqual(ex.flights_from([("BLR", "DEL")], "XXX"), [])
        mem = ex.memory_bytes(2000, 6000)
        self.assertLess(mem["adjacency list"], mem["adjacency matrix"])

    def test_solutions(self) -> None:
        self.assertEqual(sol.common_neighbours_matrix([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 0, 1), 1)
        self.assertEqual(sol.best_representation(10**6, 3 * 10**6, False), "adjacency list")
        self.assertEqual(sol.best_representation(100, 50, True), "adjacency matrix")


if __name__ == "__main__":
    unittest.main()
