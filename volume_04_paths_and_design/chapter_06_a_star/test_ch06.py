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
        g = ex.grid_graph(40, ex.GAP_WALLS)
        d = ex.a_star(g, ex.GAP_START, ex.GAP_GOAL, lambda v: 0)
        a = ex.a_star(g, ex.GAP_START, ex.GAP_GOAL, ex.grid_distance(ex.GAP_GOAL))
        self.assertEqual((d[0], len(d[2]), a[0], len(a[2])), (59, 1167, 59, 60))
        g = ex.grid_graph(40, ex.POCKET_WALLS)
        d = ex.a_star(g, ex.POCKET_START, ex.POCKET_GOAL, lambda v: 0)
        a = ex.a_star(g, ex.POCKET_START, ex.POCKET_GOAL, ex.grid_distance(ex.POCKET_GOAL))
        self.assertEqual((d[0], len(d[2]), a[0], len(a[2])), (61, 1579, 61, 669))
        o = ex.grid_graph(40, set())
        d = ex.a_star(o, (20, 0), (20, 39), lambda v: 0)
        a = ex.a_star(o, (20, 0), (20, 39), lambda v: abs(v[0] - 20) + abs(v[1] - 39))
        self.assertEqual((len(d[2]), len(a[2])), (1181, 40))


    def test_consistency(self) -> None:
        adj, s = ex.weighted_adjacency(), ex.speed_limit()
        h = lambda v: s * ex.crow_flies(v, "Harbour")
        self.assertEqual(ex.inconsistent_roads(adj, h), [])
        self.assertGreaterEqual(min(min(d.values()) for d in ex.reduced_costs(adj, h).values()), 0)
        # A* is Dijkstra on reduced costs: the same expansion order
        red = ex.a_star(ex.reduced_costs(adj, h), "Library", "Harbour", lambda v: 0)
        self.assertEqual(red[2], ex.a_star(adj, "Library", "Harbour", h)[2])
        self.assertAlmostEqual(red[0], 15 - h("Library"))
        self.assertEqual(ex.inconsistent_roads(ex.TRAP, ex.TRAP_H.get), [("A", "C")])
        exact = ex.true_remaining(ex.TRAP, "Goal")
        self.assertTrue(all(ex.TRAP_H[v] <= exact[v] for v in ex.TRAP))            # admissible
        closed = ex.a_star(ex.TRAP, "Start", "Goal", ex.TRAP_H.get)
        again = ex.a_star(ex.TRAP, "Start", "Goal", ex.TRAP_H.get, reopen=True)
        self.assertEqual(closed, (6, ["Start", "C", "Goal"], ["Start", "C", "A", "Goal"]))
        self.assertEqual(again, (5, ["Start", "A", "C", "Goal"], ["Start", "C", "A", "C", "Goal"]))
        over = ex.a_star(adj, "Library", "Harbour", lambda v: 10 * ex.crow_flies(v, "Harbour"), reopen=True)
        self.assertEqual(over[0], 16)                                             # reopening cannot cure overestimates
        perfect = ex.true_remaining(adj, "Harbour")
        self.assertEqual(ex.a_star(adj, "Library", "Harbour", perfect.get)[2],
                         ["Library", "Park", "Hospital", "Museum", "Harbour"])
        self.assertEqual(ex.a_star({"A": {}}, "A", "A", lambda v: 0, reopen=True)[:2], (0, ["A"]))
        for fix in ({"A": 1}, {"C": 3}):                                          # Practice Problem 3
            h2 = dict(ex.TRAP_H, **fix)
            self.assertEqual(ex.inconsistent_roads(ex.TRAP, h2.get), [])
            self.assertEqual(ex.a_star(ex.TRAP, "Start", "Goal", h2.get)[0], 5)
        lib_park = ex.reduced_costs(adj, h)["Library"]["Park"]
        self.assertAlmostEqual(lib_park, 1.2, places=1)


if __name__ == "__main__":
    unittest.main()
