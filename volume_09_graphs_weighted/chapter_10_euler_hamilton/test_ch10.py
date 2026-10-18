import itertools
import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


def brute_euler(edges):
    """Is there an ordering of all directed edges forming one walk?"""
    for perm in itertools.permutations(range(len(edges))):
        if all(edges[perm[i]][1] == edges[perm[i + 1]][0] for i in range(len(perm) - 1)):
            return True
    return len(edges) == 0


def brute_ham(n, edges):
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return n == 0 or any(all(p[i + 1] in adj[p[i]] for i in range(n - 1)) for p in itertools.permutations(range(n)))


class TestEulerHamilton(unittest.TestCase):
    def test_euler_random(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            n = rng.randint(1, 4)
            edges = [(rng.randrange(n), rng.randrange(n)) for _ in range(rng.randint(0, 6))]
            path = ex.hierholzer(edges)
            exists = brute_euler(edges)
            if not edges:
                continue
            self.assertEqual(path is not None, exists)
            if path:
                used = list(zip(path, path[1:]))
                self.assertEqual(sorted(used), sorted(edges))

    def test_hamilton_and_tsp(self) -> None:
        rng = random.Random(2)
        for _ in range(100):
            n = rng.randint(1, 6)
            edges = [tuple(rng.sample(range(n), 2)) for _ in range(rng.randint(0, 8))] if n > 1 else []
            self.assertEqual(ex.hamiltonian_path_exists(n, edges), brute_ham(n, edges))
        for _ in range(50):
            n = rng.randint(1, 6)
            d = [[0 if i == j else rng.randint(1, 30) for j in range(n)] for i in range(n)]
            self.assertEqual(ex.shortest_tour(d), sol.brute_force_tour(d))

    def test_examples(self) -> None:
        self.assertEqual(ex.itinerary([("MUC", "LHR"), ("JFK", "MUC"), ("SFO", "SJC"), ("LHR", "SFO")], "JFK"),
                         ["JFK", "MUC", "LHR", "SFO", "SJC"])
        self.assertEqual(ex.itinerary([("JFK", "SFO"), ("JFK", "ATL"), ("SFO", "ATL"), ("ATL", "JFK"), ("ATL", "SFO")], "JFK"),
                         ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"])
        bridges = [("N", "I"), ("N", "I"), ("S", "I"), ("S", "I"), ("N", "E"), ("S", "E"), ("I", "E")]
        self.assertFalse(sol.undirected_euler_possible(bridges))
        s = sol.de_bruijn(3)
        self.assertEqual(len(s), 10)
        self.assertEqual({s[i:i + 3] for i in range(len(s) - 2)}, {"".join(p) for p in itertools.product("01", repeat=3)})
        self.assertEqual(ex.shortest_tour([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]), 80)


if __name__ == "__main__":
    unittest.main()
