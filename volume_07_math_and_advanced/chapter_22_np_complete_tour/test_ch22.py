import itertools
import unittest

import ch22_examples as ex


class TestChapter22(unittest.TestCase):
    def test_examples(self) -> None:
        self.assertEqual(ex.satisfiable([[1, 2], [-1, 3], [-2, -3], [2, 3]], 3), ({1: False, 2: True, 3: False}, 3))
        self.assertEqual(ex.colouring(ex.TOWN, ex.ROADS, 2), (None, 256))
        c, tried = ex.colouring(ex.TOWN, ex.ROADS, 3)
        self.assertEqual((tried, all(c[a] != c[b] for a, b in ex.ROADS)), (1036, True))
        self.assertEqual((ex.vertex_cover(ex.TOWN, ex.ROADS, 3), ex.vertex_cover(ex.TOWN, ex.ROADS, 4)), (None, ["School", "Park", "Station", "Museum"]))
        self.assertEqual((ex.bin_packing([5, 4, 4, 3, 2, 2], 10, 2), ex.bin_packing([6, 6, 6], 10, 2)), ([0, 1, 1, 0, 0, 1], None))

    def test_every_case(self) -> None:
        self.assertEqual((ex.satisfiable([[1], [-1]], 1), ex.satisfiable([], 0)), ((None, 2), ({}, 1)))
        self.assertEqual((ex.colouring([], [], 1), ex.vertex_cover(["a", "b"], [], 0), ex.bin_packing([], 10, 1)), (({}, 1), [], []))
        self.assertIsNone(ex.bin_packing([11], 10, 3))


class TestReductions(unittest.TestCase):
    def random_3sat(self, r, n, m):
        return [[r.choice([1, -1]) * r.randint(1, n) for _ in range(3)] for _ in range(m)]

    def test_sat_to_independent_set(self) -> None:
        V, E, m = ex.sat_to_independent_set(ex.EXAMPLE)
        self.assertEqual((len(V), len(E), m), (9, 15, 3))
        chosen = ex.independent_set(V, E, m)
        val = ex.assignment_from_set(chosen, 3)
        self.assertTrue(all(any(val[abs(l)] == (l > 0) for l in c) for c in ex.EXAMPLE))
        import random
        r = random.Random(24)
        for _ in range(150):
            n, m = r.randint(1, 4), r.randint(1, 5)
            f = self.random_3sat(r, n, m)
            V, E, k = ex.sat_to_independent_set(f)
            self.assertEqual(ex.independent_set(V, E, k) is not None, ex.satisfiable(f, n)[0] is not None)

    def test_sat_to_colouring(self) -> None:
        import random
        r = random.Random(25)
        for _ in range(150):
            n, m = r.randint(1, 3), r.randint(1, 4)
            f = self.random_3sat(r, n, m)
            self.assertEqual(ex.three_colourable(*ex.sat_to_colouring(f, n)), ex.satisfiable(f, n)[0] is not None)

    def test_ham_to_tsp_and_table(self) -> None:
        dist, n = ex.ham_to_tsp(ex.TOWN, ex.ROADS)
        self.assertEqual(ex.shortest_round(ex.TOWN, dist)[0], 8)
        import random
        r = random.Random(26)
        for _ in range(100):
            vs = list(range(r.randint(3, 6)))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.5]
            d, nn = ex.ham_to_tsp(vs, es)
            self.assertEqual(ex.hamiltonian_cycle(vs, es) is not None, ex.shortest_round(vs, d)[0] == nn)
        self.assertEqual((ex.subset_sum_table([12, 7, 15, 9, 4, 11, 6, 13, 8, 5], 31), ex.subset_sum_table([], 0)), ((True, 230), (True, 0)))
        self.assertEqual(ex.complement_edges(["a", "b", "c"], [("a", "b")]), [("a", "c"), ("b", "c")])
        self.assertEqual(ex.cover_from_independent(ex.TOWN, ["Library", "Market", "Hospital", "Harbour"]), ["School", "Park", "Station", "Museum"])


    def test_vertex_cover_to_ham(self) -> None:
        cases = [(2, [(0, 1)]), (3, [(0, 1), (1, 2)]), (3, [(0, 1), (1, 2), (0, 2)]),
                 (4, [(0, 1), (1, 2), (2, 3)]), (4, [(0, 1), (0, 2), (0, 3)])]
        for n, edges in cases:
            for k in range(1, n + 1):
                g = ex.vertex_cover_to_ham(n, edges, k)
                self.assertEqual(len(g), 12 * len(edges) + k)
                self.assertEqual(ex.has_ham_cycle(g), ex.has_cover(n, edges, k), (n, edges, k))


if __name__ == "__main__":
    unittest.main()
