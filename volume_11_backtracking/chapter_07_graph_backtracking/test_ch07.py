import itertools
import random
import unittest

import ch07_examples as ex
import ch07_solutions as sol


def random_graph(rng, n, m):
    g = {v: [] for v in range(n)}
    for _ in range(m):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b and b not in g[a]:
            g[a].append(b)
            g[b].append(a)
    return g


def brute_chromatic(g):
    vs = list(g)
    for k in range(1, len(vs) + 1):
        for assign in itertools.product(range(k), repeat=len(vs)):
            c = dict(zip(vs, assign))
            if all(c[u] != c[v] for u in g for v in g[u]):
                return k
    return 0


def brute_ham_cycle(g):
    vs = list(g)
    if len(vs) < 3:
        return False
    for p in itertools.permutations(vs[1:]):
        cyc = [vs[0], *p, vs[0]]
        if all(b in g[a] for a, b in zip(cyc, cyc[1:])):
            return True
    return False


class TestGraphBacktracking(unittest.TestCase):
    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            g = random_graph(rng, rng.randint(1, 7), rng.randint(0, 14))
            chi = ex.chromatic_number(g)
            self.assertEqual(chi, brute_chromatic(g))
            col = ex.m_coloring(g, chi)
            self.assertTrue(sol.is_proper_coloring(g, col))
            if chi > 1:
                self.assertIsNone(ex.m_coloring(g, chi - 1))
                self.assertEqual(sol.count_colorings(g, chi - 1), 0)
            self.assertGreater(sol.count_colorings(g, chi), 0)
            if len(g) >= 3:
                cyc = ex.hamiltonian_cycle(g)
                self.assertEqual(cyc is not None, brute_ham_cycle(g))
                if cyc:
                    self.assertEqual(sorted(cyc[:-1]), sorted(g))
                    self.assertTrue(all(b in g[a] for a, b in zip(cyc, cyc[1:])))

    def test_examples(self) -> None:
        tour = ex.knights_tour(6)
        self.assertEqual(len(set(tour)), 36)
        self.assertTrue(all(sorted((abs(a[0] - b[0]), abs(a[1] - b[1]))) == [1, 2] for a, b in zip(tour, tour[1:])))
        self.assertIsNone(ex.knights_tour(3))
        regs = ex.undirected([("x", "y"), ("y", "z"), ("x", "z"), ("z", "w")])
        self.assertIsNotNone(ex.register_allocation(regs, 3))
        self.assertIsNone(ex.register_allocation(regs, 2))
        tri = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
        self.assertEqual(sol.count_colorings(tri, 3), 6)
        self.assertEqual(len(sol.all_hamiltonian_paths(tri, "a")), 2)


if __name__ == "__main__":
    unittest.main()
