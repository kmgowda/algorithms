import random
import unittest

import ch27_examples as ex


class TestChapter56(unittest.TestCase):
    def test_every_case(self) -> None:
        self.assertEqual(ex.UnionFind([]).groups, 0)
        u = ex.UnionFind("ABCD")
        self.assertEqual((u.groups, u.same("A", "A"), u.union("A", "A"), u.groups), (4, True, False, 4))
        self.assertEqual((u.union("A", "B"), u.union("B", "A"), u.groups), (True, False, 3))
        self.assertEqual((u.union("C", "D"), u.union("A", "D"), u.groups, u.same("B", "C")), (True, True, 1, True))
        with self.assertRaises(KeyError):
            u.find("Z")
        n = ex.NaiveUnionFind(range(1000))
        f = ex.UnionFind(range(1000))
        for i in range(999):
            n.union(i, i + 1)
            f.union(i, i + 1)
        self.assertEqual(n.find(0)[1], 999)
        self.assertEqual(max(ex.depth(f.parent, x) for x in range(1000)), 1)
        self.assertEqual(ex.connect_routes(4, [(1, 2), (2, 3), (3, 4)]), ([], 2))
        self.assertEqual(ex.connect_routes(4, [(1, 2), (2, 1), (3, 4)]), ([(2, 1)], None))
        self.assertEqual(ex.connect_routes(3, [(1, 2), (2, 3), (1, 3)]), ([(1, 3)], 1))
        self.assertEqual((ex.connect_routes(3, []), ex.connect_routes(1, [])), (([], None), ([], None)))

    def test_against_brute_force(self) -> None:
        rng = random.Random(1)
        n = 40
        uf = ex.UnionFind(range(n))
        groups = [{i} for i in range(n)]
        for _ in range(300):
            a, b = rng.randrange(n), rng.randrange(n)
            if rng.random() < 0.5:
                uf.union(a, b)
                ga = next(g for g in groups if a in g)
                gb = next(g for g in groups if b in g)
                if ga is not gb:
                    groups.remove(gb)
                    ga |= gb
            same = any(a in g and b in g for g in groups)
            self.assertEqual(uf.same(a, b), same)
            self.assertEqual(uf.groups, len(groups))

    def test_progression(self) -> None:
        q = ex.QuickFind("ABCDEF")
        writes = []
        for a, b in zip("ABCDE", "BCDEF"):
            q.union(a, b)
            writes.append(q.writes)
        self.assertEqual(writes, [1, 3, 6, 10, 15])
        self.assertEqual((q.union("A", "F"), q.find("A")), (False, "F"))
        self.assertEqual((ex.QuickFind([]).writes, ex.QuickFind([1]).union(1, 1)), (0, False))
        qu = ex.NaiveUnionFind("ABCDEF")
        for a, b in zip("ABCDE", "BCDEF"):
            qu.union(a, b)
        self.assertEqual(qu.find("A"), ("F", 5))
        line = ex.QuickFind(range(10_000))
        for i in range(9_999):
            line.union(i, i + 1)
        self.assertEqual(line.writes, 49_995_000)

    def test_rank_and_halving(self) -> None:
        r = ex.UnionByRank("A")
        self.assertEqual((r.find("A"), r.union("A", "A"), r.rank["A"]), ("A", False, 0))
        r = ex.UnionByRank("ABCDEFGH")
        for a, b in [("A", "B"), ("C", "D"), ("A", "C"), ("E", "F"), ("G", "H"), ("E", "G"), ("A", "E")]:
            self.assertTrue(r.union(a, b))
        self.assertEqual((r.rank["A"], r.parent), (3, {"A": "A", "B": "A", "C": "A", "D": "C", "E": "A", "F": "E",
                                                         "G": "E", "H": "G"}))
        self.assertEqual((r.union("H", "B"), r.union("B", "H")), (False, False))
        h = ex.UnionByRank("ABCDE")
        h.parent = {"A": "A", "B": "A", "C": "B", "D": "C", "E": "D"}
        self.assertEqual(h.find("E"), "A")
        self.assertEqual(h.parent, {"A": "A", "B": "A", "C": "A", "D": "C", "E": "C"})
        h = ex.UnionByRank("ABCDEFG")
        h.parent = {"A": "A", "B": "A", "C": "B", "D": "C", "E": "D", "F": "E", "G": "F"}
        h.find("G")
        self.assertEqual((h.parent["G"], h.parent["E"], h.parent["C"], h.parent["F"], h.parent["D"]),
                         ("E", "C", "A", "E", "C"))
        self.assertEqual(ex.min_members_by_rank(4), [1, 2, 4, 8, 16])
        rng = random.Random(1)
        big = ex.UnionByRank(range(100_000))
        for _ in range(200_000):
            big.union(rng.randrange(100_000), rng.randrange(100_000))
        self.assertEqual(max(big.rank.values()), 7)
        sizes = {}
        for x in range(100_000):
            root = big.find(x)
            sizes[root] = sizes.get(root, 0) + 1
        for root, size in sizes.items():
            self.assertGreaterEqual(size, 2 ** big.rank[root])          # the rank lemma
        rng = random.Random(3)
        uf, br = ex.UnionFind(range(50)), ex.UnionByRank(range(50))
        for _ in range(200):
            a, b = rng.randrange(50), rng.randrange(50)
            self.assertEqual(uf.union(a, b), br.union(a, b))
            self.assertEqual(uf.same(a, b), br.find(a) == br.find(b))

    def test_alpha(self) -> None:
        self.assertEqual([ex.ackermann_level(k, 1, 10 ** 100) for k in range(4)], [2, 3, 7, 2047])
        self.assertEqual([ex.inverse_ackermann(m) for m in (1, 2, 3, 4, 7, 8, 2047, 2048, 10 ** 9, 10 ** 80)],
                         [0, 0, 1, 2, 2, 3, 3, 4, 4, 4])

    def test_examples(self) -> None:
        uf = ex.UnionFind("ABCDEF")
        for a, b in [("A", "B"), ("C", "D"), ("B", "D"), ("E", "F")]:
            uf.union(a, b)
        self.assertEqual(uf.groups, 2)
        self.assertEqual(uf.parent["C"], "A")
        self.assertEqual(ex.connect_routes(6, [(1, 2), (2, 3), (4, 5), (3, 1), (5, 6), (3, 4)]), ([(3, 1)], 5))
        good = ex.UnionFind(range(10_000))
        for i in range(9_999):
            good.union(i, i + 1)
        self.assertEqual(max(ex.depth(good.parent, i) for i in range(10_000)), 1)


if __name__ == "__main__":
    unittest.main()
