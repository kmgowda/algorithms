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


if __name__ == "__main__":
    unittest.main()
