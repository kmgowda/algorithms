import itertools
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


def random_digraph(rng, n, m):
    g = {v: [] for v in range(n)}
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if b not in g[a]:
            g[a].append(b)
    return g


def brute_has_order(g):
    return any(sol.is_valid_order(g, list(p)) for p in itertools.permutations(g))


class TestTopo(unittest.TestCase):
    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            g = random_digraph(rng, rng.randint(1, 6), rng.randint(0, 9))
            acyclic = brute_has_order(g)
            self.assertEqual(ex.has_cycle_directed(g), not acyclic)
            for order in (ex.topological_sort_kahn(g), ex.topological_sort_dfs(g)):
                if acyclic:
                    self.assertTrue(sol.is_valid_order(g, order))
                else:
                    self.assertIsNone(order)

    def test_undirected_cycles(self) -> None:
        rng = random.Random(2)
        for _ in range(200):
            n = rng.randint(1, 8)
            edges = {tuple(sorted((rng.randrange(n), rng.randrange(n)))) for _ in range(rng.randint(0, 9))}
            edges = {e for e in edges if e[0] != e[1]}
            g = {v: [] for v in range(n)}
            for a, b in edges:
                g[a].append(b)
                g[b].append(a)
            parent = list(range(n))

            def find(x):
                while parent[x] != x:
                    x = parent[x]
                return x
            cyclic = False
            for a, b in edges:
                if find(a) == find(b):
                    cyclic = True
                parent[find(a)] = find(b)
            self.assertEqual(ex.has_cycle_undirected(g), cyclic)

    def test_examples(self) -> None:
        self.assertEqual(ex.course_order(4, [(1, 0), (2, 0), (3, 1), (3, 2)]), [0, 1, 2, 3])
        self.assertEqual(ex.course_order(2, [(0, 1), (1, 0)]), [])
        order = ex.build_order({"app": ["ui", "db"], "ui": ["widgets"], "db": ["driver"], "widgets": [], "driver": []})
        self.assertLess(order.index("widgets"), order.index("ui"))
        self.assertEqual(order[-1], "app")
        long_chain = {i: [i + 1] for i in range(5000)} | {5000: []}
        self.assertFalse(ex.has_cycle_directed(long_chain))
        self.assertEqual(ex.topological_sort_dfs(long_chain)[:3], [0, 1, 2])


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        self.assertTrue(sol.can_finish(2, [(1, 0)]))
        self.assertFalse(sol.can_finish(2, [(1, 0), (0, 1)]))
        self.assertEqual(sol.semesters_needed(3, [(2, 0), (2, 1)]), 2)
        self.assertEqual(sol.semesters_needed(2, [(0, 1), (1, 0)]), -1)
        self.assertEqual(sol.alien_alphabet(["wrt", "wrf", "er", "ett", "rftt"]), "wertf")
        self.assertEqual(sol.alien_alphabet(["abc", "ab"]), "")


if __name__ == "__main__":
    unittest.main()
