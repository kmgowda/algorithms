import random
import sys
import unittest

import ch21_examples as ex
import ch21_solutions as sol


class TestChapter18Solutions(unittest.TestCase):
    def test_same_times_as_recursion(self) -> None:
        adj = ex.adjacency()
        r, it = ex.dfs(adj, "Library"), sol.dfs_times_iterative(adj, "Library")
        self.assertEqual((it["disc"], it["fin"], it["parent"]), (r["disc"], r["fin"], r["parent"]))
        self.assertEqual(sol.dfs_times_iterative({"A": []}, "A"), {"disc": {"A": 1}, "fin": {"A": 2},
                                                                  "parent": {"A": None}})
        q = sol.dfs_times_iterative(ex.QUARTER, "Library")
        self.assertEqual({v: (q["disc"][v], q["fin"][v]) for v in q["disc"]},
                         {"Library": (1, 10), "School": (2, 5), "Market": (3, 4), "Park": (6, 9), "Hospital": (7, 8)})
        random.seed(5)
        for _ in range(200):
            n = random.randint(1, 8)
            adj = {i: [j for j in range(n) if random.random() < 0.35] for i in range(n)}
            r, it = ex.dfs(adj, 0), sol.dfs_times_iterative(adj, 0)
            self.assertEqual((it["disc"], it["fin"]), (r["disc"], r["fin"]))

    def test_deep_chain(self) -> None:
        n = 5000
        chain = ex.adjacency(list(range(n)), [(i, i + 1) for i in range(n - 1)])
        old = sys.getrecursionlimit()
        sys.setrecursionlimit(1000)
        try:
            it = sol.dfs_times_iterative(chain, 0)
        finally:
            sys.setrecursionlimit(old)
        self.assertEqual((it["disc"][n - 1], it["fin"][n - 1], it["fin"][0]), (n, n + 1, 2 * n))

    def test_parallel_roads(self) -> None:
        two = {"A": ["B", "B"], "B": ["A", "A"]}
        back = [e for e in ex.dfs(two, "A")["edges"] if e[2] == "back"]
        self.assertEqual(back, [])                       # the bug: skipping the parent by name hides the cycle
        self.assertTrue(sol.has_cycle_undirected(two, "A"))
        self.assertFalse(sol.has_cycle_undirected({"A": ["B"], "B": ["A"]}, "A"))
        self.assertFalse(sol.has_cycle_undirected({"A": []}, "A"))
        self.assertTrue(sol.has_cycle_undirected({"A": ["A", "A"]}, "A"))
        self.assertTrue(sol.has_cycle_undirected(ex.adjacency(), "Library"))
        tree = ex.adjacency(list("ABCD"), [("A", "B"), ("A", "C"), ("C", "D")])
        self.assertFalse(sol.has_cycle_undirected(tree, "A"))
        random.seed(11)
        for _ in range(300):                              # agrees with "roads >= places" on connected pieces
            n = random.randint(1, 7)
            roads = [(random.randrange(n), random.randrange(n)) for _ in range(random.randint(0, n))]
            adj = ex.adjacency(list(range(n)), roads)
            piece = set(ex.dfs_iterative(adj, 0))
            e = sum(1 for a, b in roads if a in piece)
            self.assertEqual(sol.has_cycle_undirected(adj, 0), e >= len(piece))


if __name__ == "__main__":
    unittest.main()
