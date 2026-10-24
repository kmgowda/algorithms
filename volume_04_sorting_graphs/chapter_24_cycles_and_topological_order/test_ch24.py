import itertools
import unittest

import ch24_examples as ex


class TestChapter27(unittest.TestCase):
    def test_atlas(self) -> None:
        g = ex.graph()
        log = []
        order = ex.kahn(g, log)
        self.assertEqual(order, ex.TASKS)
        self.assertEqual(log[1], ("Clean pages", ["Mend tears", "Dry pages"]))
        dfs, cycle = ex.dfs_order(g)
        self.assertIsNone(cycle)
        self.assertTrue(ex.is_valid_order(g, dfs))
        self.assertEqual(dfs[2:4], ["Dry pages", "Mend tears"])
        self.assertEqual(sum(ex.is_valid_order(g, list(p)) for p in itertools.permutations(ex.TASKS)), 2)

    def test_cycle(self) -> None:
        bad = ex.graph(needs=ex.NEEDS + [("Label", "Clean pages")])
        log = []
        self.assertIsNone(ex.kahn(bad, log))
        self.assertEqual([v for v, _ in log], ["Remove cover"])
        self.assertEqual(ex.dfs_order(bad)[1], ["Clean pages", "Mend tears", "Resew spine", "Glue spine", "New cover",
                                                "Label", "Clean pages"])

    def test_every_case(self) -> None:
        free = {"A": [], "B": [], "C": []}
        self.assertEqual(ex.kahn(free), ["A", "B", "C"])
        self.assertEqual(sum(ex.is_valid_order(free, list(p)) for p in itertools.permutations("ABC")), 6)
        self.assertEqual(ex.kahn({"A": ["B"], "B": ["C"], "C": []}), ["A", "B", "C"])
        two = {"A": ["B"], "B": [], "X": ["Y"], "Y": []}
        self.assertEqual((ex.kahn(two), ex.dfs_order(two)[0]), (["A", "X", "B", "Y"], ["X", "Y", "A", "B"]))
        self.assertEqual((ex.kahn({"A": ["A"]}), ex.dfs_order({"A": ["A"]})[1]), (None, ["A", "A"]))
        loop = {"A": ["B"], "B": ["C"], "C": ["A"], "D": ["A"]}
        self.assertIsNone(ex.kahn(loop))
        self.assertEqual(ex.dfs_order(loop)[1], ["A", "B", "C", "A"])
        self.assertEqual(ex.kahn({}), [])


    def test_closure(self) -> None:
        import random
        g = ex.graph()
        c = ex.closure(g)
        self.assertEqual(len(c["Remove cover"]), 7)
        self.assertEqual(c["Label"], set())
        self.assertEqual(c["Dry pages"], {"Resew spine", "Glue spine", "New cover", "Label"})
        self.assertNotIn("Dry pages", c["Mend tears"])
        self.assertEqual(sum(len(v) for v in c.values()), 27)
        self.assertEqual(ex.closure_in_order(g, ex.kahn(g)), c)
        r = random.Random(24)
        for _ in range(100):
            n = r.randint(1, 7)
            h = {k: [b for b in range(n) if b > k and r.random() < 0.3] for k in range(n)}
            reach = {k: set() for k in range(n)}
            for k in reversed(range(n)):          # direct definition: follow arrows step by step
                frontier = set(h[k])
                while frontier:
                    reach[k] |= frontier
                    frontier = {w for v in frontier for w in h[v]} - reach[k]
            self.assertEqual(ex.closure(h), reach)
            self.assertEqual(ex.closure_in_order(h, list(range(n))), reach)


if __name__ == "__main__":
    unittest.main()
