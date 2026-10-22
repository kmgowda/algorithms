import unittest

import ch19_examples as ex


class TestChapter22(unittest.TestCase):
    def test_lists_and_handshake(self) -> None:
        adj = ex.adjacency()
        self.assertEqual(adj["Library"], ["School", "Park"])
        self.assertEqual(adj["Market"], ["School", "Park", "Station", "Museum"])
        self.assertEqual(sum(ex.degree_table(adj).values()), 2 * len(ex.ROADS))

    def test_explore(self) -> None:
        log = []
        order = ex.explore(ex.adjacency(), "Library", log)
        self.assertEqual(order, ["Library", "Park", "Hospital", "Museum", "Station", "Harbour", "Market", "School"])
        self.assertEqual(log[3], ("Museum", ["School", "Market", "Harbour", "Station"]))

    def test_every_case(self) -> None:
        adj = ex.adjacency()
        self.assertEqual(ex.explore(adj, "Harbour"),
                         ["Harbour", "Museum", "Hospital", "Park", "Library", "School", "Market", "Station"])
        island = ex.adjacency(ex.PLACES + ["Island"], ex.ROADS)
        self.assertNotIn("Island", ex.reachable(island, "Library"))
        self.assertEqual(ex.explore(island, "Island"), ["Island"])
        self.assertEqual(ex.explore(ex.adjacency(["A", "B"], [("A", "A", 1), ("A", "B", 2)]), "A"), ["A", "B"])
        self.assertEqual(ex.explore(ex.adjacency(["A", "B"], [("A", "B", 1), ("A", "B", 2)]), "A"), ["A", "B"])
        self.assertEqual(ex.explore({"Library": []}, "Library"), ["Library"])

    def test_stack_walk_is_not_dfs(self) -> None:
        adj = ex.adjacency()
        t = ex.walk_tree(adj, "Library")
        self.assertEqual((t["Market"], t["Station"], t["Harbour"]), ("Park", "Museum", "Museum"))
        cross = ex.cross_roads(adj, t)
        self.assertIn(("Market", "Station"), cross)
        self.assertEqual(len(cross), 5)
        self.assertEqual(ex.walk_tree({"A": []}, "A"), {"A": None})
        self.assertEqual(ex.cross_roads({"A": []}, {"A": None}), [])
        self.assertTrue(ex.is_ancestor(t, "Library", "Station"))
        self.assertFalse(ex.is_ancestor(t, "Market", "Station"))

    def test_closed_roads(self) -> None:
        closed = {("Station", "Harbour"), ("Museum", "Harbour"), ("Market", "Museum")}
        roads = [r for r in ex.ROADS if (r[0], r[1]) not in closed]
        self.assertNotIn("Harbour", ex.reachable(ex.adjacency(ex.PLACES, roads), "Library"))


if __name__ == "__main__":
    unittest.main()
