import itertools
import unittest

import ch08_examples as ex


class TestChapter8(unittest.TestCase):
    def test_town(self) -> None:
        log = []
        k = ex.kruskal(ex.PLACES, ex.ROADS, log)
        self.assertEqual((ex.total(k), len(k), ex.total(ex.ROADS)), (25, 7, 56))
        self.assertEqual([r[:2] for r in log if not r[3]], [("School", "Market"), ("Park", "Hospital"), ("Market", "Museum"),
                                                           ("Station", "Harbour"), ("School", "Station")])
        p = ex.prim(ex.PLACES, ex.ROADS, "Library")
        self.assertEqual((ex.total(p), p[:3]), (25, [("Library", "Park", 3), ("Library", "School", 4), ("Park", "Market", 4)]))
        trees = [c for c in itertools.combinations(ex.ROADS, 7) if len(ex.kruskal(ex.PLACES, list(c))) == 7]
        self.assertEqual((len(trees), min(ex.total(t) for t in trees)), (244, 25))

    def test_every_case(self) -> None:
        self.assertEqual(ex.kruskal(["A", "B", "C"], [("A", "B", 1)]), [("A", "B", 1)])      # a forest: C is cut off
        self.assertEqual((ex.kruskal(["A"], []), ex.prim(["A"], [], "A")), ([], []))
        self.assertEqual(ex.kruskal(["A", "B", "C"], [("A", "B", 2), ("B", "C", 2), ("A", "C", 2)]),
                         [("A", "B", 2), ("B", "C", 2)])
        self.assertEqual(ex.total(ex.kruskal(["A", "B", "C"], [("A", "B", -1), ("B", "C", 3), ("A", "C", 2)])), 1)
        closed = [r for r in ex.ROADS if r[:2] != ("Station", "Museum")]
        self.assertEqual(ex.total(ex.kruskal(ex.PLACES, closed)), 26)
        self.assertEqual(ex.prim(ex.PLACES, ex.ROADS, "Station")[0], ("Station", "Market", 3))
        for s in ex.PLACES:
            self.assertEqual(ex.total(ex.prim(ex.PLACES, ex.ROADS, s)), 25)


    def test_more_methods(self) -> None:
        log = []
        b = ex.boruvka(ex.PLACES, ex.ROADS, log)
        self.assertEqual((ex.total(b), [len(r) for r in log]), (25, [5, 2]))
        self.assertEqual(log[1], [("Park", "Market", 4), ("Station", "Museum", 4)])
        for s in ex.PLACES:
            self.assertEqual(ex.total(ex.prim_dense(ex.PLACES, ex.ROADS, s)), 25)
        self.assertEqual(ex.prim_dense(ex.PLACES, ex.ROADS, "Library")[:3],
                         [("Library", "Park", 3), ("Library", "School", 4), ("Park", "Market", 4)])
        self.assertEqual(len(ex.minimum_trees(ex.PLACES, ex.ROADS)), 1)
        self.assertEqual(sorted(r[:2] for r in ex.heaviest_on_loops(ex.PLACES, ex.ROADS)),
                         sorted(r[:2] for r in ex.ROADS if r not in ex.kruskal(ex.PLACES, ex.ROADS)))
        self.assertEqual(ex.clusters(ex.PLACES, ex.ROADS, 2),
                         ([["Library", "School", "Park", "Market", "Station"], ["Museum", "Hospital", "Harbour"]], 4))
        self.assertEqual(ex.clusters(ex.PLACES, ex.ROADS, 3)[1], 4)
        self.assertEqual(ex.clusters(ex.PLACES, ex.ROADS, 8), ([[p] for p in ex.PLACES], 3))
        self.assertEqual(ex.clusters(ex.PLACES, ex.ROADS, 1)[1], float("inf"))
        tri = [("A", "B", 2), ("B", "C", 2), ("A", "C", 2)]
        self.assertEqual(len(ex.minimum_trees(["A", "B", "C"], tri)), 3)                 # ties: three trees
        self.assertEqual(ex.heaviest_on_loops(["A", "B", "C"], tri), [])
        # smallest inputs
        self.assertEqual((ex.boruvka(["A"], []), ex.prim_dense(["A"], [], "A")), ([], []))
        self.assertEqual(ex.prim_dense(["A", "B", "C"], [("A", "B", 1)], "A"), [("A", "B", 1)])
        self.assertEqual(ex.boruvka(["A", "B", "C"], [("A", "B", 1)]), [("A", "B", 1)])
        for seed in range(30):
            roads = ex.random_map(12, 25, seed)
            ps = list(range(12))
            t = ex.total(ex.kruskal(ps, roads))
            self.assertEqual({t}, {ex.total(ex.prim(ps, roads, 0)), ex.total(ex.prim_dense(ps, roads, 0)),
                                   ex.total(ex.boruvka(ps, roads))})
        closed = [r for r in ex.ROADS if r[:2] != ("Station", "Museum")]
        log = []
        self.assertEqual(ex.total(ex.boruvka(ex.PLACES, closed, log)), 26)                # Practice Problem 2
        self.assertEqual(log[1], [("Park", "Market", 4), ("Park", "Hospital", 5)])
        self.assertEqual(ex.clusters(ex.PLACES, ex.ROADS, 4),
                         ([["Library", "School", "Park"], ["Market", "Station"], ["Museum", "Harbour"], ["Hospital"]], 4))
        self.assertEqual(set(ex.race(200, 600)), {"Kruskal", "Prim, heap", "Prim, array"})


if __name__ == "__main__":
    unittest.main()
