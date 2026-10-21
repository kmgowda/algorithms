import unittest

import ch24_examples as ex


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
        with self.assertRaises(RecursionError):
            ex.dfs(chain, 0)
        self.assertEqual(len(ex.dfs_iterative(chain, 0)), 5000)
        self.assertEqual(len(ex.find_path(ex.adjacency(), "Library", "Harbour")) - 1, 6)


if __name__ == "__main__":
    unittest.main()
