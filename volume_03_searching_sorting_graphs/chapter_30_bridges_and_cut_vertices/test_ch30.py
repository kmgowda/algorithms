import random
import unittest

import ch30_examples as ex


class TestChapter30(unittest.TestCase):
    def test_district(self) -> None:
        big = ex.adjacency(ex.PLACES + ex.OUTER, ex.ROADS + ex.OUTER_ROADS)
        r = ex.weak_links(big)
        self.assertEqual(r["bridges"], [("Harbour", "Lighthouse"), ("Hospital", "Farm")])
        self.assertEqual(r["cuts"], ["Hospital", "Harbour"])
        self.assertEqual((r["low"]["Station"], r["low"]["Lighthouse"]), (2, 9))
        fixed = ex.adjacency(ex.PLACES + ex.OUTER, ex.ROADS + ex.OUTER_ROADS + [("Lighthouse", "Farm")])
        self.assertEqual((ex.weak_links(fixed)["bridges"], ex.weak_links(fixed)["cuts"]), ([], []))

    def test_every_case(self) -> None:
        A = ex.adjacency
        town = ex.weak_links(A(ex.PLACES, ex.ROADS))
        self.assertEqual((town["bridges"], town["cuts"]), ([], []))
        closed = ex.weak_links(A(ex.PLACES, [r for r in ex.ROADS if r != ("Library", "Park")]))
        self.assertEqual((closed["bridges"], closed["cuts"]), ([("Library", "School")], ["School"]))
        tree = ex.weak_links(A("ABCD", [("A", "B"), ("B", "C"), ("B", "D")]))
        self.assertEqual((len(tree["bridges"]), tree["cuts"]), (3, ["B"]))
        self.assertEqual(ex.weak_links(A("ABCD", [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]))["bridges"], [])
        edge = ex.weak_links(A("AB", [("A", "B")]))
        self.assertEqual((edge["bridges"], edge["cuts"]), ([("A", "B")], []))
        bow = ex.weak_links(A("ABCDE", [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("E", "C")]))
        self.assertEqual((bow["bridges"], bow["cuts"]), ([], ["C"]))
        self.assertEqual(ex.weak_links(A("A", []))["cuts"], [])

    def test_against_brute_force(self) -> None:
        rng = random.Random(3)
        for _ in range(150):
            n = rng.randint(1, 9)
            names = [str(i) for i in range(n)]
            roads = {tuple(sorted(rng.sample(names, 2))) for _ in range(rng.randint(0, 12)) if n > 1}
            adj = ex.adjacency(names, sorted(roads))
            r, b = ex.weak_links(adj), ex.brute_force(adj)
            self.assertEqual({frozenset(x) for x in r["bridges"]}, b["bridges"])
            self.assertEqual(set(r["cuts"]), b["cuts"])


if __name__ == "__main__":
    unittest.main()
