import itertools
import random
import unittest

import ch28_examples as ex
import ch28_solutions as sol


def brute_girth(names, roads):
    """Try every ordered set of 3 or more distinct places as a cycle."""
    edges = {frozenset(r) for r in roads}
    for k in range(3, len(names) + 1):
        for cyc in itertools.permutations(names, k):
            if all(frozenset((cyc[i], cyc[(i + 1) % k])) in edges for i in range(k)):
                return k
    return None


class TestChapter25Solutions(unittest.TestCase):
    def test_girth_examples(self) -> None:
        A, W = ex.bfs_m.adjacency, ex.weak_m
        self.assertEqual(sol.girth(A()), 3)
        self.assertEqual(sol.girth(A(ex.PLACES + W.OUTER, ex.ROADS + W.OUTER_ROADS)), 3)
        self.assertEqual(sol.girth(A("ABCD", [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])), 4)
        self.assertEqual(sol.girth(A("ABCDE", [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "A")])), 5)
        self.assertIsNone(sol.girth(A("ABCD", [("A", "B"), ("B", "C"), ("B", "D")])))
        club = ex.bip_m.adjacency(ex.bip_m.MEMBERS, ex.bip_m.QUARRELS)
        self.assertEqual(sol.girth(club), 4)

    def test_girth_smallest(self) -> None:
        self.assertIsNone(sol.girth({}))
        self.assertIsNone(sol.girth({"A": []}))
        self.assertIsNone(sol.girth(ex.bfs_m.adjacency("AB", [("A", "B")])))

    def test_girth_random_against_brute_force(self) -> None:
        rng = random.Random(25)
        for _ in range(200):
            n = rng.randint(1, 7)
            names = [str(i) for i in range(n)]
            roads = sorted({tuple(sorted(rng.sample(names, 2))) for _ in range(rng.randint(0, 10)) if n > 1})
            self.assertEqual(sol.girth(ex.bfs_m.adjacency(names, roads)), brute_girth(names, roads))

    def test_back_roads(self) -> None:
        A, W = ex.bfs_m.adjacency, ex.weak_m
        self.assertEqual(sol.back_road_count(A()), 5)
        self.assertEqual(sol.back_road_count(A(ex.PLACES + W.OUTER, ex.ROADS + W.OUTER_ROADS)), 5)
        self.assertEqual(sol.back_road_count({}), 0)
        adj = A()
        for start in ex.PLACES:                       # every start gives the same number of back roads
            d = ex.dfs_m.dfs(adj, start)
            self.assertEqual(sum(1 for e in d["edges"] if e[2] == "back"), 5)

    def test_flawed_cycle_test(self) -> None:
        g = {"A": ["B", "C"], "B": [], "C": ["B"]}
        self.assertTrue(sol.has_cycle_seen_test(g))
        self.assertIsNotNone(ex.topo_m.kahn(g))          # but there is no cycle: a topological order exists
        self.assertFalse(sol.has_cycle_seen_test({}))
        self.assertFalse(sol.has_cycle_seen_test({"A": []}))


if __name__ == "__main__":
    unittest.main()
