import unittest

import ch06_examples as ex


class TestChapter6(unittest.TestCase):
    def test_town(self) -> None:
        adj, s = ex.weighted_adjacency(), ex.speed_limit()
        self.assertAlmostEqual(s, 2.04, places=2)
        d = ex.a_star(adj, "Library", "Harbour", lambda v: 0)
        a = ex.a_star(adj, "Library", "Harbour", lambda v: s * ex.crow_flies(v, "Harbour"))
        self.assertEqual((d[0], a[0], a[1]), (15, 15, ["Library", "Park", "Hospital", "Museum", "Harbour"]))
        self.assertEqual((len(d[2]), len(a[2])), (8, 8))
        for a_, b_, w in ex.ROADS:
            self.assertLessEqual(s * ex.crow_flies(a_, b_), w + 1e-9)

    def test_every_case(self) -> None:
        adj, s = ex.weighted_adjacency(), ex.speed_limit()
        self.assertEqual(ex.a_star(adj, "Library", "Library", lambda v: 0)[:2], (0, ["Library"]))
        island = ex.weighted_adjacency(ex.PLACES + ["Island"], ex.ROADS)
        self.assertEqual(ex.a_star(island, "Library", "Island", lambda v: 0)[:2], (float("inf"), None))
        over = ex.a_star(adj, "Library", "Harbour", lambda v: 10 * ex.crow_flies(v, "Harbour"))
        self.assertEqual((over[0], len(over[2])), (16, 5))
        walls = {(r, 20) for r in range(5, 40)}
        g = ex.grid_graph(40, walls)
        d = ex.a_star(g, (39, 0), (0, 39), lambda v: 0)
        a = ex.a_star(g, (39, 0), (0, 39), lambda v: abs(v[0]) + abs(v[1] - 39))
        self.assertEqual((d[0], len(d[2]), a[0], len(a[2])), (78, 1128, 78, 79))
        o = ex.grid_graph(40, set())
        d = ex.a_star(o, (20, 0), (20, 39), lambda v: 0)
        a = ex.a_star(o, (20, 0), (20, 39), lambda v: abs(v[0] - 20) + abs(v[1] - 39))
        self.assertEqual((len(d[2]), len(a[2])), (1181, 40))


if __name__ == "__main__":
    unittest.main()
