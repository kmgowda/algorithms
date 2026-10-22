import unittest

import ch05_examples as ex


class TestChapter5(unittest.TestCase):
    def test_town(self) -> None:
        dist, nxt = ex.town_table()
        self.assertEqual(dist[0], [0, 4, 3, 7, 10, 12, 8, 15])
        self.assertEqual(dist[3], [7, 5, 4, 0, 3, 6, 9, 9])
        self.assertEqual([ex.PLACES[i] for i in ex.path(nxt, 0, 7)], ["Library", "Park", "Hospital", "Museum", "Harbour"])
        self.assertEqual([max(r) for r in dist], [15, 14, 12, 9, 10, 12, 12, 15])
        self.assertEqual([sum(r) for r in dist], [59, 61, 47, 43, 46, 49, 53, 66])
        inf = float("inf")
        self.assertEqual(ex.entry_history(0, 7), [inf, inf, inf, inf, inf, 16, 16, 15, 15])
        self.assertTrue(all(dist[i][j] == dist[j][i] for i in range(8) for j in range(8)))

    def test_every_case(self) -> None:
        d, _ = ex.floyd_warshall(3, [(0, 1, 1), (1, 2, -3), (2, 1, 1)], directed=True)
        self.assertTrue(ex.has_negative_cycle(d))
        d, n = ex.floyd_warshall(3, [(0, 1, 2)])
        self.assertEqual((d[0][2], ex.path(n, 0, 2), ex.path(n, 1, 1)), (float("inf"), None, [1]))
        self.assertEqual(ex.floyd_warshall(1, [])[0], [[0]])
        self.assertEqual(ex.floyd_warshall(2, [(0, 1, 5), (0, 1, 3)])[0], [[0, 3], [3, 0]])
        d, _ = ex.floyd_warshall(3, [(0, 1, 4), (1, 2, -2), (0, 2, 5)], directed=True)
        self.assertEqual((d[0][2], ex.has_negative_cycle(d)), (2, False))

    def test_johnson(self) -> None:
        dist, h = ex.johnson(ex.DEPOTS, ex.LEGS)
        self.assertEqual(h, {"A": -7, "B": -5, "C": 0, "D": -3, "E": -9})
        re = ex.reweight(ex.LEGS, h)
        self.assertTrue(all(w >= 0 for _, _, w in re))
        self.assertEqual([w for _, _, w in re], [4, 0, 3, 3, 0, 0, 18, 0, 1, 0])
        self.assertEqual(dist["A"], {"A": 0, "B": 2, "C": 7, "D": 4, "E": -2})
        self.assertEqual((dist["D"]["A"], dist["C"]["A"]), (-4, -7))
        self.assertEqual(max(re, key=lambda e: e[2]), ("C", "E", 18))
        index = {v: i for i, v in enumerate(ex.DEPOTS)}
        fw, _ = ex.floyd_warshall(5, [(index[a], index[b], w) for a, b, w in ex.LEGS], directed=True)
        self.assertEqual([[dist[a][b] for b in ex.DEPOTS] for a in ex.DEPOTS], fw)
        self.assertIsNone(ex.johnson(["A", "B"], [("A", "B", -1), ("B", "A", 0)]))
        self.assertEqual(ex.johnson([], []), ({}, {}))
        self.assertEqual(ex.johnson(["A"], []), ({"A": {"A": 0}}, {"A": 0}))
        self.assertEqual(ex.johnson(["A", "B"], [("A", "B", -1)])[0]["B"]["A"], float("inf"))
        _, nxt = ex.town_table()
        self.assertEqual(ex.route_by_next_hop(nxt, ex.PLACES, "School", "Harbour"),
                         ["School", "Market", "Station", "Harbour"])

if __name__ == "__main__":
    unittest.main()
