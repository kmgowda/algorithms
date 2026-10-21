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


if __name__ == "__main__":
    unittest.main()
