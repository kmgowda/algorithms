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


    def test_sat_to_subset_sum(self) -> None:
        nums, target = ex.sat_to_subset_sum(ex.EXAMPLE, 3)
        self.assertEqual(target, 111444)
        self.assertEqual(len(nums), 2 * 3 + 2 * 3)
        self.assertEqual(dict(nums)["x1"], 100101)
        self.assertEqual(dict(nums)["not x2"], 10011)
        chosen = ex.subset_with_sum(nums, target)
        self.assertEqual(sum(dict(nums)[c] for c in chosen), target)
        setting = {v: f"x{v}" in chosen for v in range(1, 4)}
        self.assertTrue(all(any(setting[abs(l)] == (l > 0) for l in c) for c in ex.EXAMPLE))
        self.assertIsNone(ex.subset_with_sum(*ex.sat_to_subset_sum([[1, 1, 1], [-1, -1, -1]], 1)))
        import random
        r = random.Random(22)
        for _ in range(150):
            n = r.randint(1, 4)
            clauses = [[r.choice([1, -1]) * r.randint(1, n) for _ in range(3)] for _ in range(r.randint(1, 5))]
            nums, target = ex.sat_to_subset_sum(clauses, n)
            self.assertEqual(ex.subset_with_sum(nums, target) is not None, ex.satisfiable(clauses, n)[0] is not None)

    def test_subset_sum_to_partition(self) -> None:
        import random
        r = random.Random(7)
        for _ in range(300):
            vals = [r.randint(1, 12) for _ in range(r.randint(0, 7))]
            t = r.randint(0, sum(vals))
            direct = ex.subset_with_sum([(str(i), v) for i, v in enumerate(vals)], t) is not None
            self.assertEqual(ex.can_partition(ex.subset_sum_to_partition(vals, t)), direct, (vals, t))
        self.assertEqual(ex.subset_sum_to_partition([3, 5, 9], 8), [3, 5, 9, 26, 25])
        self.assertTrue(ex.can_partition([3, 5, 9, 26, 25]))
        self.assertFalse(ex.can_partition(ex.subset_sum_to_partition([3, 5, 9], 7)))


if __name__ == "__main__":
    unittest.main()
