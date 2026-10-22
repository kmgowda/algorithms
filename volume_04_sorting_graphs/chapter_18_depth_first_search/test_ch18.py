import sys
import unittest

import ch18_examples as ex


class TestChapter24(unittest.TestCase):
    def test_dfs(self) -> None:
        r = ex.dfs(ex.adjacency(), "Library")
        self.assertEqual(r["order"], ["Library", "School", "Market", "Park", "Hospital", "Museum", "Harbour", "Station"])
        self.assertEqual((r["disc"]["Station"], r["fin"]["Station"], r["fin"]["Library"]), (8, 9, 16))
        back = [(a, b) for a, b, k in r["edges"] if k == "back"]
        self.assertEqual(len(back), 5)
        self.assertEqual(ex.dfs_iterative(ex.adjacency(), "Library"), r["order"])

    def test_parenthesis(self) -> None:
        r = ex.dfs(ex.adjacency(), "Library")
        for a in r["disc"]:
            for b in r["disc"]:
                da, fa, db, fb = r["disc"][a], r["fin"][a], r["disc"][b], r["fin"][b]
                self.assertTrue(fa < db or fb < da or (da < db and fb < fa) or (db < da and fa < fb) or a == b)

    def test_every_case(self) -> None:
        self.assertEqual(ex.dfs({"Library": []}, "Library")["fin"], {"Library": 2})
        island = ex.adjacency(ex.PLACES + ["Island"], ex.ROADS)
        self.assertIsNone(ex.find_path(island, "Library", "Island"))
        self.assertEqual(ex.dfs(island, "Island")["order"], ["Island"])
        tree = ex.dfs(ex.adjacency(["A", "B", "C", "D"], [("A", "B"), ("A", "C"), ("C", "D")]), "A")
        self.assertEqual([e for e in tree["edges"] if e[2] == "back"], [])
        loop = ex.dfs(ex.adjacency(["A", "B"], [("A", "A"), ("A", "B")]), "A")
        self.assertIn(("A", "A", "back"), loop["edges"])
        chain = ex.adjacency(list(range(5000)), [(i, i + 1) for i in range(4999)])
        old = sys.getrecursionlimit()
        sys.setrecursionlimit(1000)                 # Python's default; other modules may have raised it
        try:
            with self.assertRaises(RecursionError):
                ex.dfs(chain, 0)
        finally:
            sys.setrecursionlimit(old)
        self.assertEqual(len(ex.dfs_iterative(chain, 0)), 5000)
        self.assertEqual(len(ex.find_path(ex.adjacency(), "Library", "Harbour")) - 1, 6)

    def test_directed_classification(self) -> None:
        c = ex.classify_directed(ex.QUARTER)
        kinds = {(a, b): k for a, b, k in c["edges"]}
        self.assertEqual(kinds, {("Library", "School"): "tree", ("School", "Market"): "tree",
                                 ("Market", "Library"): "back", ("Library", "Park"): "tree",
                                 ("Park", "Market"): "cross", ("Park", "Hospital"): "tree",
                                 ("Library", "Market"): "forward"})
        self.assertEqual((c["disc"]["Park"], c["fin"]["Park"], c["fin"]["Library"]), (6, 9, 10))
        self.assertEqual(ex.classify_directed({}), {"disc": {}, "fin": {}, "edges": []})
        self.assertEqual(ex.classify_directed({"A": ["A"]})["edges"], [("A", "A", "back")])
        two = ex.classify_directed({"A": [], "B": ["A"]})        # a restart: B -> A goes to another tree
        self.assertEqual(two["edges"], [("B", "A", "cross")])

    def test_other_order(self) -> None:
        q = dict(ex.QUARTER, Library=["Market", "Park", "School"])
        kinds = {(a, b): k for a, b, k in ex.classify_directed(q)["edges"]}
        self.assertEqual((kinds[("Library", "Market")], kinds[("School", "Market")], kinds[("Market", "Library")]),
                         ("tree", "cross", "back"))
        self.assertNotIn("forward", kinds.values())

    def test_white_path(self) -> None:
        q = ex.QUARTER
        self.assertEqual(ex.white_path_descendants(q, "Park", {"Library", "School", "Market"}), {"Park", "Hospital"})
        self.assertEqual(ex.white_path_descendants(q, "Library", set()), set(q))
        self.assertEqual(ex.white_path_descendants({"A": []}, "A", set()), {"A"})
        c = ex.classify_directed(q)
        for u in q:                                       # the theorem, checked against the real DFS
            before = {v for v in q if c["disc"][v] < c["disc"][u]}
            desc = {v for v in q if c["disc"][u] <= c["disc"][v] and c["fin"][v] <= c["fin"][u]}
            self.assertEqual(ex.white_path_descendants(q, u, before), desc)


if __name__ == "__main__":
    unittest.main()
