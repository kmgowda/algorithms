import unittest

import ch11_examples as ex


class TestChapter11(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
