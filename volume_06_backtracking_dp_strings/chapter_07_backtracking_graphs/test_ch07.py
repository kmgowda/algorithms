import unittest

import ch07_examples as ex


class TestChapter31(unittest.TestCase):
    def test_town(self) -> None:
        got = [ex.colour(ex.PLACES, ex.ROADS, k) for k in (1, 2, 3)]
        self.assertEqual([(c is None, n) for c, n in got], [(True, 2), (True, 9), (False, 9)])
        col = got[2][0]
        self.assertTrue(all(col[a] != col[b] for a, b in ex.ROADS))
        routes, nodes = ex.hamiltonian(ex.PLACES, ex.ROADS, "Library")
        self.assertEqual((len(routes), nodes), (10, 99))
        self.assertEqual(sum(len(ex.hamiltonian(ex.PLACES, ex.ROADS, s)[0]) for s in ex.PLACES), 56)
        self.assertEqual(len(ex.hamiltonian(ex.PLACES, ex.ROADS, "Harbour")[0]), 13)
        col, n = ex.colour(ex.PLACES, ex.ROADS + [("Library", "Market")], 3)
        self.assertEqual((col["Market"], col["Harbour"], n), (2, 2, 9))

    def test_every_case(self) -> None:
        self.assertEqual((ex.colour([], [], 0), ex.colour(["A"], [], 1), ex.colour(["A", "B"], [("A", "B")], 1)),
                         (({}, 1), ({"A": 0}, 2), (None, 2)))
        self.assertEqual(ex.colour(["A", "B", "C"], [("A", "B"), ("B", "C"), ("A", "C")], 2), (None, 5))
        self.assertEqual(ex.hamiltonian(["A"], [], "A"), ([["A"]], 1))
        self.assertEqual(ex.hamiltonian(["A", "B", "C"], [("A", "B"), ("A", "C")], "B"), ([["B", "A", "C"]], 3))
        self.assertEqual(ex.hamiltonian(["A", "B", "C", "D"], [("A", "B"), ("A", "C"), ("A", "D")], "A"), ([], 4))


    def test_dead_end_pruning(self) -> None:
        routes, nodes = ex.hamiltonian_pruned(ex.PLACES, ex.ROADS, "Library")
        self.assertEqual((routes, nodes), (ex.hamiltonian(ex.PLACES, ex.ROADS, "Library")[0], 80))
        places, roads = ex.grid_map(4, 5)
        plain, pruned = ex.hamiltonian(places, roads, (0, 0)), ex.hamiltonian_pruned(places, roads, (0, 0))
        self.assertEqual((len(plain[0]), plain[1], len(pruned[0]), pruned[1]), (160, 13591, 160, 3266))
        self.assertEqual(sorted(plain[0]), sorted(pruned[0]))
        self.assertEqual(ex.hamiltonian_pruned(["A"], [], "A"), ([["A"]], 1))
        self.assertEqual(ex.hamiltonian_pruned(["A", "B", "C", "D"], [("A", "B"), ("A", "C"), ("A", "D")], "B"), ([], 4))
        found, n = ex.hamiltonian_first(places, roads, (0, 0))
        self.assertEqual(found, plain[0][0])

    def test_ordering(self) -> None:
        self.assertEqual([ex.fewest_colours(ex.PLACES, ex.ROADS, o) for o in ("list", "degree", "dsatur")],
                         [(3, 20), (3, 16), (3, 16)])
        places, roads = ex.random_graph(30, 0.3, 3)
        self.assertEqual(len(roads), 122)
        self.assertEqual([ex.fewest_colours(places, roads, o) for o in ("list", "degree", "dsatur")],
                         [(5, 271705), (5, 4687), (5, 437)])
        col, _ = ex.colour_ordered(places, roads, 5, "dsatur")
        self.assertTrue(all(col[a] != col[b] for a, b in roads))
        self.assertEqual(ex.fewest_colours([], [], "dsatur"), (0, 1))
        self.assertEqual([ex.colour_ordered(ex.PLACES, ex.ROADS, 2, o)[1] for o in ("list", "degree", "dsatur")], [9, 5, 5])


if __name__ == "__main__":
    unittest.main()
