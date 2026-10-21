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


if __name__ == "__main__":
    unittest.main()
