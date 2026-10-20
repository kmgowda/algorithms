import random
import unittest

import ch56_examples as ex


class TestChapter56(unittest.TestCase):
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
