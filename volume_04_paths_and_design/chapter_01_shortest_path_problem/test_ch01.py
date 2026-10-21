import itertools
import unittest

import ch01_examples as ex


class TestChapter1(unittest.TestCase):
    def test_town(self) -> None:
        adj = ex.weighted_adjacency()
        bfs = ex.fewest_roads_route(adj, "Library", "Harbour")
        self.assertEqual((bfs, ex.route_length(adj, bfs)), (["Library", "School", "Station", "Harbour"], 19))
        self.assertEqual(ex.shortest_by_brute_force(adj, "Library", "Harbour"),
                         (15, ["Library", "Park", "Hospital", "Museum", "Harbour"], 20))
        best = {g: ex.shortest_by_brute_force(adj, "Library", g)[0] for g in ex.PLACES}
        self.assertEqual(best, {"Library": 0, "School": 4, "Park": 3, "Market": 7, "Station": 10, "Museum": 12,
                                "Hospital": 8, "Harbour": 15})

    def test_every_case(self) -> None:
        adj = ex.weighted_adjacency()
        self.assertEqual(ex.shortest_by_brute_force(adj, "Library", "Library")[:2], (0, ["Library"]))
        self.assertEqual(ex.route_length(adj, ["Library", "Harbour"]), float("inf"))
        island = ex.weighted_adjacency(ex.PLACES + ["Island"], ex.ROADS)
        self.assertEqual(ex.shortest_by_brute_force(island, "Library", "Island"), (float("inf"), None, 0))
        zero = ex.weighted_adjacency(["A", "B", "C"], [("A", "B", 0), ("B", "C", 2), ("A", "C", 2)])
        self.assertEqual(sorted(ex.route_length(zero, r) for r in ex.all_routes(zero, "A", "C")), [2, 2])
        neg = ex.weighted_adjacency(["A", "B", "C"], [("A", "B", 5), ("B", "C", -4), ("A", "C", 2)])
        self.assertEqual(ex.shortest_by_brute_force(neg, "A", "C")[:2], (1, ["A", "B", "C"]))
        counts = []
        for n in (4, 6, 8):
            p = [str(i) for i in range(n)]
            a = ex.weighted_adjacency(p, [(x, y, 1) for x, y in itertools.combinations(p, 2)])
            counts.append(sum(1 for _ in ex.all_routes(a, "0", str(n - 1))))
        self.assertEqual(counts, [5, 65, 1957])


if __name__ == "__main__":
    unittest.main()
