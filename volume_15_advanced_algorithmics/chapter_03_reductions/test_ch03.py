import itertools
import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol


def random_graph(rng, n, p=0.5):
    g = {v: set() for v in range(n)}
    for u, v in itertools.combinations(range(n), 2):
        if rng.random() < p:
            g[u].add(v)
            g[v].add(u)
    return g


def has_ham_cycle(g):
    nodes = list(g)
    if len(nodes) < 3:
        return False
    first = nodes[0]
    return any(all(b in g[a] for a, b in zip((first,) + p, p + (first,))) for p in itertools.permutations(nodes[1:]))


def has_ham_path(g):
    return any(all(b in g[a] for a, b in zip(p, p[1:])) for p in itertools.permutations(g)) if g else False


class TestReductions(unittest.TestCase):
    def test_reductions_preserve_answers(self) -> None:
        rng = random.Random(1)
        for _ in range(60):
            n = rng.randint(1, 6)
            g = random_graph(rng, n)
            k = rng.randint(0, n)
            g2, k2 = ex.vertex_cover_to_independent_set(g, k)
            self.assertEqual(ex.has_vertex_cover(g, k), ex.has_independent_set(g2, k2))
            g3, k3 = ex.independent_set_to_clique(g, k)
            self.assertEqual(ex.has_independent_set(g, k), ex.has_clique(g3, k3))
            if n <= 4:
                for c in (1, 2, 3):
                    clauses, nv = ex.coloring_to_sat(g, c)
                    self.assertEqual(ex.is_colorable(g, c), ex.brute_sat(clauses, nv))
            if 2 <= n <= 5:
                self.assertEqual(has_ham_path(g), has_ham_cycle(sol.hamiltonian_path_to_cycle(g)))
        for _ in range(60):
            nv = rng.randint(1, 4)
            clauses = [tuple(rng.choice([1, -1]) * rng.randint(1, nv) for _ in range(rng.randint(1, 5))) for _ in range(rng.randint(1, 4))]
            three, total = sol.sat_to_3sat(clauses, nv)
            self.assertTrue(all(len(c) == 3 for c in three))
            self.assertEqual(ex.brute_sat(clauses, nv), ex.brute_sat(three, total))
            vals = [rng.randint(1, 9) for _ in range(rng.randint(1, 6))]
            t = rng.randint(0, sum(vals))
            sub = any(sum(c) == t for r in range(len(vals) + 1) for c in itertools.combinations(vals, r))
            items = sol.subset_sum_to_partition(vals, t)
            part = any(2 * sum(c) == sum(items) for r in range(len(items) + 1) for c in itertools.combinations(items, r))
            self.assertEqual(sub, part)

    def test_examples(self) -> None:
        self.assertEqual(ex.meeting_rooms_to_coloring([(9, 10), (9, 11), (10, 12)]), {0: {1}, 1: {0, 2}, 2: {1}})
        clauses, n = ex.coloring_to_sat({0: {1, 2}, 1: {0, 2}, 2: {0, 1}}, 3)
        self.assertEqual((len(clauses), n), (21, 9))


if __name__ == "__main__":
    unittest.main()
