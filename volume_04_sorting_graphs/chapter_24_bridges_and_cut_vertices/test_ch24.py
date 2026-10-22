import random
import unittest

import ch24_examples as ex


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

    def test_parallel_roads(self) -> None:
        A = ex.adjacency
        two = ex.weak_links(A("AB", [("A", "B"), ("A", "B")]))
        self.assertEqual((two["bridges"], two["cuts"]), ([], []))
        tail = ex.weak_links(A("ABC", [("A", "B"), ("A", "B"), ("B", "C")]))
        self.assertEqual((tail["bridges"], tail["cuts"]), ([("B", "C")], ["B"]))
        self.assertEqual(ex.brute_force(A("AB", [("A", "B"), ("A", "B")]))["bridges"], set())
        loop = ex.weak_links(A("AB", [("A", "A"), ("A", "B")]))
        self.assertEqual(loop["bridges"], [("A", "B")])

    def test_blocks(self) -> None:
        A = ex.adjacency
        big = A(ex.PLACES + ex.OUTER, ex.ROADS + ex.OUTER_ROADS)
        got = [sorted(ex.block_places(b)) for b in ex.blocks(big)]
        self.assertEqual(got, [["Harbour", "Lighthouse"], ["Farm", "Hospital"], sorted(ex.PLACES)])
        bow = A("ABCDE", [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("E", "C")])
        bs, joins = ex.block_cut_tree(bow)
        self.assertEqual(bs, [{"C", "D", "E"}, {"A", "B", "C"}])
        self.assertEqual(joins, [(0, "C"), (1, "C")])
        self.assertEqual(ex.blocks(A("A", [])), [])
        self.assertEqual(ex.blocks({}), [])
        self.assertEqual(ex.blocks(A("AB", [("A", "B")])), [[("A", "B")]])
        self.assertEqual(len(ex.blocks(A("AB", [("A", "B"), ("A", "B")]))), 1)

    def test_blocks_random(self) -> None:
        rng = random.Random(30)
        for _ in range(200):
            n = rng.randint(1, 8)
            names = [str(i) for i in range(n)]
            roads = sorted({tuple(sorted(rng.sample(names, 2))) for _ in range(rng.randint(0, 11)) if n > 1})
            adj = ex.adjacency(names, roads)
            bs = ex.blocks(adj)
            edges = [frozenset(e) for b in bs for e in b]
            self.assertEqual(sorted(edges, key=sorted), sorted((frozenset(r) for r in roads), key=sorted))
            counts = {}
            for b in bs:
                for p in ex.block_places(b):
                    counts[p] = counts.get(p, 0) + 1
            self.assertEqual({p for p, c in counts.items() if c >= 2}, set(ex.weak_links(adj)["cuts"]))
            for b in bs:                                   # a block with 3 or more places has no cut vertex of its own
                places = ex.block_places(b)
                if len(places) >= 3:
                    sub = ex.adjacency(sorted(places), [tuple(e) for e in b])
                    self.assertEqual(ex.weak_links(sub)["cuts"], [])

    def test_parallel_random_against_brute_force(self) -> None:
        rng = random.Random(31)
        for _ in range(150):
            n = rng.randint(2, 7)
            names = [str(i) for i in range(n)]
            roads = [tuple(rng.sample(names, 2)) for _ in range(rng.randint(0, 10))]
            adj = ex.adjacency(names, roads)
            r, b = ex.weak_links(adj), ex.brute_force(adj)
            self.assertEqual({frozenset(x) for x in r["bridges"]}, b["bridges"])
            self.assertEqual(set(r["cuts"]), b["cuts"])


if __name__ == "__main__":
    unittest.main()
