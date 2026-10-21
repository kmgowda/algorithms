import unittest

import ch31_examples as ex


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


if __name__ == "__main__":
    unittest.main()
