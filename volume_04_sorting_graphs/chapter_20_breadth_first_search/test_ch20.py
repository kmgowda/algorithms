import unittest

import ch20_examples as ex


class TestChapter23(unittest.TestCase):
    def test_bfs(self) -> None:
        log = []
        dist, parent = ex.bfs(ex.adjacency(), "Library", log)
        self.assertEqual(ex.layers(dist), [["Library"], ["School", "Park"], ["Market", "Station", "Hospital"],
                                           ["Museum", "Harbour"]])
        self.assertEqual(log[3], ("Market", ["Station", "Hospital", "Museum"]))
        self.assertEqual(ex.route(parent, "Harbour"), ["Library", "School", "Station", "Harbour"])

    def test_every_case(self) -> None:
        adj = ex.adjacency()
        dist, parent = ex.bfs(adj, "Library")
        self.assertEqual(ex.route(parent, "Library"), ["Library"])
        self.assertEqual(ex.route(parent, "Park"), ["Library", "Park"])
        self.assertEqual(ex.route(parent, "Museum"), ["Library", "School", "Market", "Museum"])
        counts = ex.count_shortest_routes(adj, "Library")
        self.assertEqual((counts["Market"], counts["Museum"]), (2, 4))
        island = ex.adjacency(ex.PLACES + ["Island"], ex.ROADS)
        self.assertIsNone(ex.route(ex.bfs(island, "Library")[1], "Island"))
        self.assertEqual(ex.bfs(ex.adjacency(["A", "B"], [("A", "A"), ("A", "B")]), "A")[0], {"A": 0, "B": 1})
        self.assertEqual(ex.bfs({"Library": []}, "Library")[0], {"Library": 0})

    def test_distances_are_shortest(self) -> None:
        import itertools
        adj = ex.adjacency()
        dist, _ = ex.bfs(adj, "Library")
        for v in ex.PLACES:                       # brute force over all simple paths
            best = min(len(p) for p in self._paths(adj, "Library", v))
            self.assertEqual(dist[v], best - 1)

    def _paths(self, adj, a, b, seen=None):
        seen = seen or [a]
        if a == b:
            yield list(seen)
            return
        for w in adj[a]:
            if w not in seen:
                yield from self._paths(adj, w, b, seen + [w])

    def test_from_the_market(self) -> None:
        dist, parent = ex.bfs(ex.adjacency(), "Market")
        self.assertEqual(ex.layers(dist), [["Market"], ["School", "Park", "Station", "Museum"],
                                           ["Library", "Hospital", "Harbour"]])
        self.assertEqual(ex.route(parent, "Harbour"), ["Market", "Station", "Harbour"])
        self.assertEqual(ex.route({"A": None}, "A"), ["A"])
        self.assertIsNone(ex.route({}, "A"))


if __name__ == "__main__":
    unittest.main()
