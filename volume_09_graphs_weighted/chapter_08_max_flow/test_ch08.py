import itertools
import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol


def brute_min_cut(n, edges, s, t):
    """Try every split with s on one side and t on the other."""
    others = [v for v in range(n) if v not in (s, t)]
    best = float("inf")
    for r in range(len(others) + 1):
        for side in itertools.combinations(others, r):
            S = {s, *side}
            best = min(best, sum(c for u, v, c in edges if u in S and v not in S))
    return best


class TestMaxFlow(unittest.TestCase):
    def test_max_flow_equals_min_cut(self) -> None:
        rng = random.Random(1)
        for _ in range(150):
            n = rng.randint(2, 7)
            edges = [(rng.randrange(n), rng.randrange(n), rng.randint(1, 9)) for _ in range(rng.randint(0, 14))]
            edges = [e for e in edges if e[0] != e[1]]
            net = ex.FlowNetwork()
            for v in range(n):
                net.cap.setdefault(v, {})
            for u, v, c in edges:
                net.add_edge(u, v, c)
            value, flow = net.max_flow(0, n - 1)
            self.assertEqual(value, brute_min_cut(n, edges, 0, n - 1))
            self.assertTrue(sol.check_flow(net, flow, 0, n - 1))
            side, cut = net.min_cut(0)
            self.assertEqual(sum(net.cap[u][v] for u, v in cut), value)
            self.assertNotIn(n - 1, side)

    def test_examples(self) -> None:
        net = ex.FlowNetwork()
        for u, v, c in [("S", "A", 10), ("S", "B", 5), ("A", "B", 15), ("A", "T", 5), ("B", "T", 10)]:
            net.add_edge(u, v, c)
        self.assertEqual(net.max_flow("S", "T")[0], 15)
        roads = [("Town", "Bridge", 700), ("Town", "Hill road", 300), ("Bridge", "Shelter", 500),
                 ("Hill road", "Shelter", 400), ("Bridge", "Hill road", 200)]
        self.assertEqual(ex.evacuation_capacity(roads, "Town", "Shelter")[0], 900)

    def test_solutions(self) -> None:
        self.assertEqual(sol.multi_source_flow({"F1": 10, "F2": 5}, {"Shop": 12},
                                               [("F1", "Hub", 8), ("F2", "Hub", 5), ("Hub", "Shop", 20)]), 12)
        self.assertEqual(sol.edge_disjoint_paths([("s", "a"), ("s", "b"), ("a", "t"), ("b", "t"), ("a", "b")], "s", "t"), 2)


if __name__ == "__main__":
    unittest.main()
