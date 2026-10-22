import itertools
import random
import unittest

import ch22_examples as ex
import ch22_solutions as sol


class TestThinkingProblems(unittest.TestCase):
    def test_sat_to_independent_set(self) -> None:
        r = random.Random(22)
        for _ in range(60):
            n = r.randint(1, 4)
            clauses = [[r.choice([1, -1]) * r.randint(1, n) for _ in range(r.randint(1, 3))] for _ in range(r.randint(1, 4))]
            vs, es, m = ex.sat_to_independent_set(clauses)
            self.assertEqual(ex.satisfiable(clauses, n)[0] is not None, ex.independent_set(vs, es, m) is not None)

    def test_two_colour(self) -> None:
        colour, cycle = sol.two_colour(ex.TOWN, ex.ROADS)
        self.assertIsNone(colour)
        self.assertEqual(len(cycle) % 2, 1)
        edges = {frozenset(e) for e in ex.ROADS}
        self.assertTrue(all(frozenset((cycle[i], cycle[(i + 1) % len(cycle)])) in edges for i in range(len(cycle))))
        self.assertEqual(sol.two_colour([], []), ({}, None))
        r = random.Random(2)
        for _ in range(100):
            vs = list(range(r.randint(1, 8)))
            es = [e for e in itertools.combinations(vs, 2) if r.random() < 0.3]
            colour, cycle = sol.two_colour(vs, es)
            self.assertEqual(colour is not None, ex.colouring(vs, es, 2)[0] is not None)
            if colour is not None:
                self.assertTrue(all(colour[a] != colour[b] for a, b in es))
            else:
                ce = {frozenset(e) for e in es}
                self.assertEqual(len(cycle) % 2, 1)
                self.assertTrue(all(frozenset((cycle[i], cycle[(i + 1) % len(cycle)])) in ce for i in range(len(cycle))))

    def test_greedy_order(self) -> None:
        path = [("a", "b"), ("b", "c"), ("c", "d")]
        self.assertEqual(len(set(sol.greedy_colour(list("adbc"), path).values())), 3)
        self.assertEqual(len(set(sol.greedy_colour(list("abcd"), path).values())), 2)


if __name__ == "__main__":
    unittest.main()
