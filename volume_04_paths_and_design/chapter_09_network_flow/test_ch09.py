import itertools
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
        d = [("s", "a", 1), ("a", "b", 1), ("b", "t", 1), ("s", "b", 1), ("a", "t", 1)]
        self.assertEqual((ex.greedy_no_undo(d, "s", "t"), ex.max_flow(["s", "a", "b", "t"], d, "s", "t")[0]), (1, 2))


if __name__ == "__main__":
    unittest.main()
