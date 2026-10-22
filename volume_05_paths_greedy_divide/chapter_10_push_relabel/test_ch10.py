import itertools
import random
import unittest

import ch10_examples as ex


def brute_min_cut(nodes, edges, s, t):
    mid = [v for v in nodes if v not in (s, t)]
    return min(sum(c for a, b, c in edges if a in S and b not in S)
               for k in range(len(mid) + 1) for m in itertools.combinations(mid, k) for S in [{s, *m}])


class TestChapter10(unittest.TestCase):
    def test_town(self) -> None:
        log = []
        total, flow, height = ex.push_relabel(ex.NODES, ex.PIPES, "Warehouse", "Library", log)
        self.assertEqual(total, 13)
        self.assertEqual(ex.counts(log), (18, 13))
        self.assertEqual(height, {"Warehouse": 6, "Docks": 7, "Mill": 7, "Bridge": 7, "Square": 8, "Library": 0})
        self.assertEqual(log[:2], [("push", "Warehouse", "Docks", 10), ("push", "Warehouse", "Mill", 8)])
        self.assertEqual(log[5:7], [("relabel", "Docks", 1, 7), ("push", "Docks", "Warehouse", 3)])
        self.assertEqual(sum(1 for x in log if x[0] == "relabel" and x[1] in ("Bridge", "Square")), 9)
        for v in ex.NODES[1:-1]:                                   # a real flow at the end: in = out
            self.assertEqual(sum(f for (a, b), f in flow.items() if b == v), sum(f for (a, b), f in flow.items() if a == v))
        side, cut = ex.cut_from_heights(ex.NODES, ex.PIPES, "Warehouse", "Library")
        self.assertEqual(cut, [("Bridge", "Library", 7), ("Square", "Library", 6)])
        self.assertTrue(all(height[v] >= len(ex.NODES) for v in side))   # the gap: no height from 1 to 5
        self.assertFalse(any(0 < h < 6 for h in height.values()))

    def test_every_case(self) -> None:
        f = lambda n, e: ex.push_relabel(n, e, "s", "t")
        self.assertEqual(f(["s", "t"], [])[0], 0)                           # no road out of the source
        self.assertEqual(f(["s", "t"], [("s", "t", 0)])[0], 0)              # a road of capacity 0
        log = []
        self.assertEqual(ex.push_relabel(["s", "t"], [("s", "t", 4)], "s", "t", log)[0], 4)
        self.assertEqual(log, [("push", "s", "t", 4)])                      # straight to the sink: one push
        log = []
        self.assertEqual(ex.push_relabel(["s", "a", "t"], [("s", "a", 5)], "s", "t", log)[0], 0)
        self.assertEqual(log[-1], ("push", "a", "s", 5))                    # a dead end returns everything
        log = []
        self.assertEqual(ex.push_relabel(["s", "m", "t"], [("s", "m", 5), ("m", "t", 3)], "s", "t", log)[0], 3)
        self.assertEqual(log[-1], ("push", "m", "s", 2))                    # the bottleneck sends 2 back
        cyc = [("s", "a", 4), ("a", "b", 4), ("b", "a", 4), ("b", "t", 2)]
        log = []
        self.assertEqual(ex.push_relabel(["s", "a", "b", "t"], cyc, "s", "t", log)[0], 2)
        self.assertEqual(ex.counts(log), (7, 6))
        trap = [("s", "a", 1), ("a", "b", 1), ("b", "t", 1), ("s", "b", 1), ("a", "t", 1)]
        log = []
        self.assertEqual(ex.push_relabel(["s", "a", "b", "t"], trap, "s", "t", log)[0], 2)
        self.assertIn(("push", "b", "a", 1), log)                           # the undo happens by a local push

    def test_random_against_edmonds_karp(self) -> None:
        rng = random.Random(10)
        for _ in range(300):
            n = rng.randint(2, 6)
            nodes = list(range(n))
            edges = [(a, b, rng.randint(0, 6)) for a in nodes for b in nodes if a != b and rng.random() < 0.4]
            total, flow, height = ex.push_relabel(nodes, edges, 0, n - 1)
            self.assertEqual(total, ex.edmonds_karp(nodes, edges, 0, n - 1)[0])
            self.assertEqual(total, brute_min_cut(nodes, edges, 0, n - 1))
            self.assertTrue(all(h < 2 * n for h in height.values()))       # heights stay below 2n
            side, cut = ex.cut_from_heights(nodes, edges, 0, n - 1)
            self.assertEqual(sum(c for *_, c in cut), total)
            g = ex.push_relabel_global(nodes, edges, 0, n - 1)
            self.assertEqual(g[0], total)

    def test_compare(self) -> None:
        r = ex.compare(ex.NODES, ex.PIPES, "Warehouse", "Library")
        self.assertEqual((r["flow"], r["same"], r["ek_paths"], r["pushes"], r["relabels"]), (13, True, 3, 18, 13))
        big = ex.compare(*ex.layered_network(10, 12))
        self.assertTrue(big["same"])
        self.assertLess(big["global_reads"], big["ek_reads"])
        self.assertGreater(big["pr_reads"], big["ek_reads"])
        self.assertEqual(ex.ROOM_TYPE, dict)                                 # compare() restores the plain table


if __name__ == "__main__":
    unittest.main()
