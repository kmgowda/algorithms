import itertools
import random
import unittest

import ch09_examples as ex


class TestChapter9(unittest.TestCase):
    def test_town(self) -> None:
        log = []
        total, flow = ex.max_flow(ex.NODES, ex.PIPES, "Warehouse", "Library", log)
        self.assertEqual(total, 13)
        self.assertEqual([p for _, p in log], [5, 6, 2])
        self.assertEqual(flow[("Docks", "Mill")], 0)
        side, cut = ex.min_cut(ex.NODES, ex.PIPES, "Warehouse", "Library")
        self.assertEqual((sum(c for *_, c in cut), cut), (13, [("Bridge", "Library", 7), ("Square", "Library", 6)]))
        for v in ex.NODES[1:-1]:                                     # flow in = flow out at every middle place
            self.assertEqual(sum(f for (a, b), f in flow.items() if b == v), sum(f for (a, b), f in flow.items() if a == v))
        best = min(sum(c for a, b, c in ex.PIPES if a in S and b not in S)
                   for k in range(5) for mid in itertools.combinations(ex.NODES[1:-1], k) for S in [{"Warehouse", *mid}])
        self.assertEqual(best, 13)

    def test_practice(self) -> None:
        f = lambda edges: ex.max_flow(ex.NODES, edges, "Warehouse", "Library")[0]
        self.assertEqual(f([(a, b, 7 if (a, b) == ("Square", "Library") else c) for a, b, c in ex.PIPES]), 14)
        self.assertEqual(f([e for e in ex.PIPES if e[:2] != ("Square", "Bridge")]), 11)
        self.assertEqual(f([(a, b, 1) for a, b, _ in ex.PIPES]), 2)

    def test_every_case(self) -> None:
        self.assertEqual(ex.max_flow(["s", "t"], [], "s", "t")[0], 0)
        self.assertEqual(ex.max_flow(["s", "t"], [("s", "t", 4), ("s", "t", 3)], "s", "t")[0], 7)
        self.assertEqual(ex.max_flow(["s", "t"], [("s", "t", 0)], "s", "t")[0], 0)
        self.assertEqual(ex.max_flow(["s", "m", "t"], [("s", "m", 5), ("m", "t", 3)], "s", "t")[0], 3)
        d = [("s", "a", 1), ("a", "b", 1), ("b", "t", 1), ("s", "b", 1), ("a", "t", 1)]
        self.assertEqual((ex.greedy_no_undo(d, "s", "t"), ex.max_flow(["s", "a", "b", "t"], d, "s", "t")[0]), (1, 2))

    def test_residual_and_rounds(self) -> None:
        f2 = ex.flow_after_rounds(ex.NODES, ex.PIPES, "Warehouse", "Library", 2)
        self.assertEqual(sum(f for (a, _), f in f2.items() if a == "Warehouse"), 11)
        r = ex.residual(ex.PIPES, f2)
        self.assertEqual((r[("Library", "Square")], r[("Mill", "Warehouse")], r[("Warehouse", "Mill")]), (6, 6, 2))
        self.assertNotIn(("Docks", "Bridge"), r)                    # full: no room forwards
        _, f = ex.max_flow(ex.NODES, ex.PIPES, "Warehouse", "Library")
        self.assertEqual(ex.flow_after_rounds(ex.NODES, ex.PIPES, "Warehouse", "Library", 3), f)
        self.assertEqual(sorted(p for _, p in ex.decompose(ex.PIPES, f, "Warehouse", "Library")), [2, 5, 6])

    def test_ford_fulkerson(self) -> None:
        d = [("s", "a", 1000), ("s", "b", 1000), ("a", "b", 1), ("a", "t", 1000), ("b", "t", 1000)]
        nodes = ["s", "a", "b", "t"]
        self.assertEqual(ex.ford_fulkerson(nodes, d, "s", "t", "smallest"), (2000, 2000))
        self.assertEqual(ex.ford_fulkerson(nodes, d, "s", "t"), (2000, 2))
        self.assertEqual(ex.ford_fulkerson(ex.NODES, ex.PIPES, "Warehouse", "Library"), (13, 3))
        self.assertEqual(ex.ford_fulkerson(["s", "t"], [], "s", "t"), (0, 0))

    def test_applications(self) -> None:
        paths = ex.edge_disjoint_paths(ex.NODES, ex.PIPES, "Warehouse", "Library")
        self.assertEqual(len(paths), 2)
        roads = [r for p in paths for r in zip(p, p[1:])]
        self.assertEqual(len(roads), len(set(roads)))                # no road shared
        self.assertEqual(ex.edge_disjoint_paths(["s", "t"], [], "s", "t"), [])
        self.assertEqual(ex.project_selection(ex.PROJECTS, ex.EQUIPMENT, ex.NEEDS), (3, ["Reading app", "Coding club"]))
        self.assertEqual(ex.project_selection({}, {}, {}), (0, []))
        self.assertEqual(ex.project_selection({"P": 2}, {"Q": 5}, {"P": ["Q"]}), (0, []))
        rng = random.Random(9)
        for _ in range(60):
            pr = {f"p{i}": rng.randint(0, 9) for i in range(rng.randint(0, 4))}
            eq = {f"q{i}": rng.randint(0, 9) for i in range(rng.randint(1, 4))}
            nd = {p: rng.sample(list(eq), rng.randint(0, len(eq))) for p in pr}
            self.assertEqual(ex.project_selection(pr, eq, nd)[0], ex.best_projects_brute(pr, eq, nd))


    def test_min_cost_flow(self) -> None:
        import itertools
        import random
        flow, cost, rounds = ex.min_cost_flow(ex.NODES, ex.COSTED, "Warehouse", "Library", 13)
        self.assertEqual((flow, cost), (13, 89))
        self.assertEqual([r[2] for r in rounds], [6, 7, 7, 8])
        self.assertIn(["Warehouse", "Docks", "Bridge", "Square", "Library"], [r[0] for r in rounds])
        self.assertEqual(ex.min_cost_flow(ex.NODES, ex.COSTED, "Warehouse", "Library", 10)[:2], (10, 67))
        self.assertEqual(ex.min_cost_flow(["s", "t"], [], "s", "t", 3)[:2], (0, 0))

        def brute(nodes, edges, s, t, need):
            best = None
            for f in itertools.product(*[range(c + 1) for _, _, c, _ in edges]):
                bal = {v: 0 for v in nodes}
                for (a, b, _, _), x in zip(edges, f):
                    bal[a] -= x
                    bal[b] += x
                if bal[t] == need and all(bal[v] == 0 for v in nodes if v not in (s, t)):
                    c = sum(x * w for (_, _, _, w), x in zip(edges, f))
                    best = c if best is None else min(best, c)
            return best
        r = random.Random(9)
        nodes = ["s", "a", "b", "t"]
        for _ in range(150):
            edges = [(a, b, r.randint(0, 2), r.randint(0, 5)) for a, b in itertools.permutations(nodes, 2)
                     if a != "t" and b != "s" and r.random() < 0.6]
            need = r.randint(1, 3)
            flow, cost, _ = ex.min_cost_flow(nodes, edges, "s", "t", need)
            if flow == need:
                self.assertEqual(cost, brute(nodes, edges, "s", "t", need))
            else:
                self.assertIsNone(brute(nodes, edges, "s", "t", need))


    def test_dinic_and_circulation(self) -> None:
        import random
        self.assertEqual(ex.dinic(ex.NODES, ex.PIPES, "Warehouse", "Library"), (13, 2))
        r = random.Random(19)
        nodes = list(range(6))
        for _ in range(200):
            edges = [(a, b, r.randint(1, 9)) for a in nodes for b in nodes if a != b and r.random() < 0.35]
            self.assertEqual(ex.dinic(nodes, edges, 0, 5)[0], ex.max_flow(nodes, edges, 0, 5)[0])
        self.assertTrue(ex.circulation(ex.NODES, ex.PIPES, {"Warehouse": -8, "Docks": -3, "Library": 7, "Square": 4}))
        self.assertFalse(ex.circulation(ex.NODES, ex.PIPES, {"Warehouse": -14, "Library": 14}))
        self.assertFalse(ex.circulation(ex.NODES, ex.PIPES, {"Warehouse": -5, "Library": 4}))


if __name__ == "__main__":
    unittest.main()
