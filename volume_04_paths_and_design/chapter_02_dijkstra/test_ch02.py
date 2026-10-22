import random
import unittest

import ch02_examples as ex


class TestChapter2(unittest.TestCase):
    def test_town(self) -> None:
        log = []
        dist, parent = ex.dijkstra(ex.weighted_adjacency(), "Library", log)
        self.assertEqual([v for v, _ in log], ["Library", "Park", "School", "Market", "Hospital", "Station", "Museum",
                                               "Harbour"])
        self.assertEqual(dist["Harbour"], 15)
        self.assertEqual(ex.route(parent, "Harbour"), ["Library", "Park", "Hospital", "Museum", "Harbour"])
        self.assertEqual(ex.route(parent, "Station"), ["Library", "Park", "Market", "Station"])
        self.assertEqual(ex.dijkstra_counting(ex.weighted_adjacency(), "Library")[1:], (11, 10))

    def test_every_case(self) -> None:
        adj = ex.weighted_adjacency()
        dist, parent = ex.dijkstra(adj, "Library")
        self.assertEqual((dist["Library"], ex.route(parent, "Library")), (0, ["Library"]))
        island = ex.weighted_adjacency(ex.PLACES + ["Island"], ex.ROADS)
        d, p = ex.dijkstra(island, "Library")
        self.assertEqual(("Island" in d, ex.route(p, "Island")), (False, None))
        zero = ex.weighted_adjacency(["A", "B", "C"], [("A", "B", 0), ("B", "C", 2), ("A", "C", 2)])
        self.assertEqual(ex.dijkstra(zero, "A")[0], {"A": 0, "B": 0, "C": 2})
        self.assertEqual(ex.dijkstra({"A": {}}, "A")[0], {"A": 0})
        neg = {"A": {"B": 5, "C": 2}, "B": {"C": -4}, "C": {"D": 1}, "D": {}}
        self.assertEqual(ex.dijkstra(neg, "A")[0]["D"], 3)           # wrong: the true answer is 5 - 4 + 1 = 2
        self.assertEqual(ex.dijkstra(adj, "Harbour")[0]["Library"], 15)

    def test_matches_brute_force(self) -> None:
        rng = random.Random(4)
        for _ in range(50):
            n = 6
            adj = {i: {} for i in range(n)}
            for _ in range(9):
                a, b = rng.randrange(n), rng.randrange(n)
                if a != b:
                    adj[a][b] = adj[b][a] = rng.randint(1, 9)
            best = {0: 0}
            changed = True
            while changed:                                         # simple fixed-point check
                changed = False
                for v in list(best):
                    for w, m in adj[v].items():
                        if best[v] + m < best.get(w, 1e9):
                            best[w] = best[v] + m
                            changed = True
            self.assertEqual(ex.dijkstra(adj, 0)[0], best)

    def test_counts_snapshots_and_array(self) -> None:
        adj = ex.weighted_adjacency()
        self.assertEqual(ex.offer_counts(adj, "Library"), (7, 3))
        snaps = ex.snapshots(adj, "Library")
        self.assertEqual([v for v, _, _ in snaps], ["Library", "Park", "School", "Market", "Hospital", "Station",
                                                     "Museum", "Harbour"])
        self.assertEqual(snaps[2][2]["Station"], 13)
        self.assertEqual(snaps[3][2]["Station"], 10)
        self.assertEqual(snaps[5][2]["Harbour"], 16)
        self.assertEqual(snaps[6][2]["Harbour"], 15)
        dist, looked = ex.dijkstra_array(adj, "Library")
        self.assertEqual((dist, looked), (ex.dijkstra(adj, "Library")[0], 36))
        self.assertEqual(ex.dijkstra_array({"A": {}}, "A"), ({"A": 0}, 1))
        self.assertEqual(ex.dijkstra_array({"A": {}, "B": {}}, "A"), ({"A": 0}, 3))
        self.assertEqual(ex.offer_counts({"A": {}}, "A"), (0, 0))

if __name__ == "__main__":
    unittest.main()
