import random
import unittest

import ch10_examples as ex
import ch10_solutions as sol


class TestChapter10Solutions(unittest.TestCase):
    def test_town(self) -> None:
        self.assertEqual(sol.push_relabel_gap(ex.NODES, ex.PIPES, "Warehouse", "Library"), (13, 13, 11))
        self.assertEqual(sol.push_relabel_low_source(ex.NODES, ex.PIPES, "Warehouse", "Library"), 0)

    def test_smallest(self) -> None:
        self.assertEqual(sol.push_relabel_gap(["s", "t"], [], "s", "t")[0], 0)
        self.assertEqual(sol.push_relabel_gap(["s", "t"], [("s", "t", 3)], "s", "t"), (3, 1, 0))
        self.assertEqual(sol.push_relabel_gap(["s", "a", "t"], [("s", "a", 5)], "s", "t")[0], 0)
        self.assertEqual(sol.push_relabel_low_source(["s", "t"], [("s", "t", 3)], "s", "t"), 3)

    def test_random(self) -> None:
        rng = random.Random(11)
        for _ in range(300):
            n = rng.randint(2, 7)
            nodes = list(range(n))
            edges = [(a, b, rng.randint(0, 6)) for a in nodes for b in nodes if a != b and rng.random() < 0.4]
            self.assertEqual(sol.push_relabel_gap(nodes, edges, 0, n - 1)[0], ex.edmonds_karp(nodes, edges, 0, n - 1)[0])

    def test_gap_saves_work(self) -> None:
        nodes, edges = ex.layered_network(10, 12)
        log = []
        ex.push_relabel(nodes, edges, "s", "t", log)
        flow, pushes, relabels = sol.push_relabel_gap(nodes, edges, "s", "t")
        self.assertEqual(flow, 123)
        self.assertLess(pushes + relabels, sum(ex.counts(log)) // 10)


if __name__ == "__main__":
    unittest.main()
