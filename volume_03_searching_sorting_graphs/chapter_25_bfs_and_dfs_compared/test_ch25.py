import unittest

import ch25_examples as ex


class TestChapter25(unittest.TestCase):
    def test_town(self) -> None:
        adj = ex.adjacency()
        b, d = ex.bfs(adj, "Library"), ex.dfs(adj, "Library")
        self.assertEqual(b["order"], ["Library", "School", "Park", "Market", "Station", "Hospital", "Museum", "Harbour"])
        self.assertEqual(d["order"], ["Library", "School", "Market", "Park", "Hospital", "Museum", "Harbour", "Station"])
        self.assertEqual(b["frontier"], [2, 3, 3, 3, 3, 2, 1, 0])
        self.assertEqual(max(d["frontier"]), 8)
        self.assertEqual((ex.summary(b)["tree height"], ex.summary(d)["tree height"]), (3, 7))

    def test_every_case(self) -> None:
        adj = ex.adjacency()
        self.assertEqual(ex.bfs(adj, "Library")["order"][0], ex.dfs(adj, "Library")["order"][0])
        island = ex.adjacency(ex.PLACES + ["Island"], ex.ROADS)
        self.assertEqual(set(ex.bfs(island, "Library")["order"]), set(ex.dfs(island, "Library")["order"]))
        self.assertNotIn("Island", ex.bfs(island, "Library")["order"])
        self.assertEqual(ex.dfs(adj, "Library")["order"].index("Station"), 7)
        star = ex.adjacency(["Hub"] + [f"S{i}" for i in range(100)], [("Hub", f"S{i}") for i in range(100)])
        line = ex.adjacency(list(range(100)), [(i, i + 1) for i in range(99)])
        self.assertEqual((ex.summary(ex.bfs(star, "Hub"))["largest frontier"],
                          ex.summary(ex.dfs(star, "Hub"))["largest frontier"]), (100, 2))
        self.assertEqual((ex.summary(ex.bfs(line, 0))["largest frontier"],
                          ex.summary(ex.dfs(line, 0))["largest frontier"]), (1, 100))


if __name__ == "__main__":
    unittest.main()
