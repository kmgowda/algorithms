import unittest

import ch12_examples as ex


class TestChapter12(unittest.TestCase):
    def test_town(self) -> None:
        deg = ex.degrees(ex.PLACES, ex.ROADS)
        self.assertEqual(sorted(p for p, d in deg.items() if d % 2), ["Park", "School"])
        self.assertEqual(ex.euler_kind(ex.PLACES, ex.ROADS), "trail")
        w = ex.euler_walk(ex.PLACES, ex.ROADS)
        self.assertEqual((len(w), w[0], w[-1]), (13, "School", "Park"))
        used = sorted(tuple(sorted(p)) for p in zip(w, w[1:]))
        self.assertEqual(used, sorted(tuple(sorted(r)) for r in ex.ROADS))
        self.assertEqual(len(ex.hamiltonian_paths(ex.PLACES, ex.ROADS)), 28)

    def test_every_case(self) -> None:
        r2 = [r for r in ex.ROADS if r != ("Station", "Museum")]
        self.assertEqual((ex.euler_kind(ex.PLACES, r2), ex.euler_walk(ex.PLACES, r2)), ("none", None))
        self.assertEqual(ex.euler_walk(["A", "B", "C"], [("A", "B"), ("B", "C"), ("C", "A")]), ["A", "C", "B", "A"])
        self.assertEqual((ex.euler_walk(["A"], []), ex.euler_walk(["A", "B"], [("A", "B")])), ([], ["A", "B"]))
        extra, pairs = ex.postman_extra(r2)
        self.assertEqual((extra, sum(ex.MINUTES[r] for r in r2)), (16, 52))
        star = (["A", "B", "C", "D"], [("A", "B"), ("A", "C"), ("A", "D")])
        self.assertEqual((ex.euler_kind(*star), ex.hamiltonian_paths(*star)), ("none", []))

    def test_splicing_and_directed(self) -> None:
        pieces, walk = ex.hierholzer_pieces(ex.PLACES, ex.ROADS)
        self.assertEqual([len(p) - 1 for p in pieces], [9, 3])
        self.assertEqual(pieces[1], ["Station", "Harbour", "Museum", "Station"])
        self.assertEqual((len(walk), walk[0], walk[-1]), (13, "School", "Park"))
        self.assertEqual(sorted(tuple(sorted(p)) for p in zip(walk, walk[1:])), sorted(tuple(sorted(r)) for r in ex.ROADS))
        self.assertEqual(ex.hierholzer_pieces(["A"], []), ([], []))
        self.assertEqual(ex.euler_walk_directed(["A", "B", "C"], [("A", "B"), ("B", "C"), ("C", "A")]), ["A", "B", "C", "A"])
        self.assertEqual(ex.euler_walk_directed(["A", "B", "C"], [("A", "B"), ("B", "C"), ("C", "A"), ("A", "C")]),
                         ["A", "B", "C", "A", "C"])
        self.assertIsNone(ex.euler_walk_directed(["A", "B"], [("A", "B"), ("A", "B")]))
        self.assertEqual(ex.euler_walk_directed(["A"], []), [])
        # two separate loops: every degree is even, but the roads are in two pieces
        two = [("A", "B"), ("B", "C"), ("C", "A"), ("D", "E"), ("E", "F"), ("F", "D")]
        self.assertEqual((ex.one_piece(two), ex.euler_kind(list("ABCDEF"), two)), (False, "none"))
        self.assertEqual(ex.euler_kind(list("ABCZ"), [("A", "B"), ("B", "C"), ("C", "A")]), "circuit")  # Z: no roads
        self.assertEqual(len(ex.hamiltonian_paths(ex.PLACES, ex.ROADS)) * 2, 56)
        self.assertEqual((ex.hamiltonian_paths(list("ABCDEF"), two), ex.hamiltonian_paths(list("ABCZ"), two[:3])), ([], []))
        self.assertEqual(ex.postman_extra(ex.ROADS), (7, [("Park", "School")]))     # Challenge 1: 56 + 7 = 63
        one_way = [("Market", "Station"), ("Station", "Museum"), ("Museum", "Market"), ("Market", "Park"),
                   ("Park", "Hospital"), ("Hospital", "Museum")]
        self.assertEqual(ex.euler_walk_directed(["Market", "Station", "Museum", "Park", "Hospital"], one_way),
                         ["Market", "Station", "Museum", "Market", "Park", "Hospital", "Museum"])


if __name__ == "__main__":
    unittest.main()
