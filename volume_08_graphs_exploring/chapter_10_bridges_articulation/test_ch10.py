import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


def random_graph(rng, n, m):
    g = {v: [] for v in range(n)}
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b and b not in g[a]:
            g[a].append(b)
            g[b].append(a)
    return g


class TestBridges(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            g = random_graph(rng, rng.randint(1, 10), rng.randint(0, 16))
            base = sol.count_components(g)
            edges = sorted({tuple(sorted((u, v))) for u in g for v in g[u]})
            brute_bridges = [e for e in edges if sol.count_components(g, removed_edge=e) > base]
            self.assertEqual(sorted(tuple(sorted(e)) for e in ex.bridges(g)), brute_bridges)
            brute_points = [v for v in g if sol.count_components(g, removed_vertex=v) > base - (1 if not g[v] else 0)]
            brute_points = [v for v in brute_points if g[v]]
            self.assertEqual(ex.articulation_points(g), sorted(brute_points, key=str))

    def test_examples(self) -> None:
        self.assertEqual(ex.critical_cables(4, [(0, 1), (1, 2), (2, 0), (1, 3)]), [(1, 3)])
        roads = [("Pune", "Lonavala"), ("Lonavala", "Mumbai"), ("Mumbai", "Thane"), ("Thane", "Lonavala"),
                 ("Pune", "Satara"), ("Satara", "Kolhapur")]
        self.assertEqual(ex.single_points_of_failure(roads), ["Lonavala", "Pune", "Satara"])
        chain = {i: [] for i in range(3000)}
        for i in range(2999):
            chain[i].append(i + 1)
            chain[i + 1].append(i)
        self.assertEqual(len(ex.bridges(chain)), 2999)

    def test_solutions(self) -> None:
        g = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
        self.assertEqual(sol.count_components(g, removed_vertex=1), 2)
        self.assertEqual(sol.two_edge_connected_groups(g), [[0, 1, 2], [3]])
        self.assertEqual(sol.cables_to_add_for_redundancy(g), 1)
        path = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
        self.assertEqual(sol.cables_to_add_for_redundancy(path), 1)
        star = {0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}
        self.assertEqual(sol.cables_to_add_for_redundancy(star), 2)


if __name__ == "__main__":
    unittest.main()
