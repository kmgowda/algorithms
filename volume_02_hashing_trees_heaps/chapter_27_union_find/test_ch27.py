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
