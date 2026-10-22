import random
import unittest

import ch16_examples as ex
import ch16_solutions as sol


class TestChapter16Solutions(unittest.TestCase):
    def test_size_and_rank_build_different_forests(self) -> None:
        unions = [(0, 1), (0, 2), (0, 3), (0, 4), (5, 6), (7, 8), (5, 7), (0, 5)]
        s, r = ex.UnionFind(range(9)), ex.UnionByRank(range(9))
        for a, b in unions:
            s.union(a, b)
            r.union(a, b)
        self.assertEqual((sol.tallest(s.parent), sol.tallest(r.parent)), (3, 2))
        self.assertEqual((s.find(8), r.find(8)), (0, 5))

    def test_rollback(self) -> None:
        uf = sol.RollbackUnionFind([])
        self.assertFalse(uf.undo())
        uf = sol.RollbackUnionFind(["A"])
        self.assertFalse(uf.union("A", "A"))
        self.assertTrue(uf.undo())                       # undoing a redundant union changes nothing
        self.assertEqual((uf.groups, uf.parent), (1, {"A": "A"}))
        uf = sol.RollbackUnionFind("ABCD")
        uf.union("A", "B")
        uf.union("C", "D")
        uf.union("B", "D")
        self.assertTrue(uf.find("D") == uf.find("A"))
        uf.undo()
        self.assertFalse(uf.find("D") == uf.find("A"))
        self.assertEqual(uf.groups, 2)
        rng = random.Random(6)
        for _ in range(50):
            n = rng.randint(1, 12)
            uf, log = sol.RollbackUnionFind(range(n)), []
            for _ in range(40):
                if log and rng.random() < 0.35:
                    log.pop()
                    uf.undo()
                else:
                    log.append((rng.randrange(n), rng.randrange(n)))
                    uf.union(*log[-1])
                fresh = ex.UnionFind(range(n))
                for a, b in log:
                    fresh.union(a, b)
                self.assertEqual(uf.groups, fresh.groups)
                for x in range(n):
                    for y in range(n):
                        self.assertEqual(uf.find(x) == uf.find(y), fresh.same(x, y))
                self.assertLessEqual(sol.tallest(uf.parent), max(1, n).bit_length() - 1)

    def test_stale_sizes_build_a_chain(self) -> None:
        bug = sol.StaleSizeUnionFind([0])
        self.assertFalse(bug.union(0, 0))
        for n in (2, 8, 50):
            bug, good = sol.StaleSizeUnionFind(range(n)), ex.UnionFind(range(n))
            for i in range(1, n):
                bug.union(i, 0)
                good.union(i, 0)
            self.assertEqual(sol.tallest(bug.parent), n - 1)
            self.assertEqual(sol.tallest(good.parent), 1)


if __name__ == "__main__":
    unittest.main()
