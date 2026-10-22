import random
import unittest

import ch24_examples as ex
import ch24_solutions as sol


class TestChapter24Solutions(unittest.TestCase):
    def test_binomial_without_decrease_key(self) -> None:
        self.assertTrue(sol.is_binomial_forest(ex.FibHeap()))            # empty heap
        self.assertTrue(sol.is_binomial_forest(ex.FibHeap([4])))         # one item: B0
        for seed in range(20):
            rng = random.Random(seed)
            h = ex.FibHeap()
            for _ in range(300):
                if rng.random() < 0.6 or not len(h):
                    h.insert(rng.randrange(100))
                else:
                    h.delete_min()
                self.assertTrue(sol.is_binomial_forest(h))
        h = ex.FibHeap(range(9))                                          # decrease-key breaks it
        nodes = list(h.nodes())
        h.delete_min()
        leaf = next(x for x in h.nodes() if x.parent is not None and x.parent.parent is not None)
        h.decrease_key(leaf, -1)
        self.assertFalse(sol.is_binomial_forest(h))

    def test_report_at_most(self) -> None:
        self.assertEqual(sol.report_at_most(ex.FibHeap(), 10), ([], 0))  # empty heap
        found, visited = sol.report_at_most(ex.FibHeap([5]), 4)          # nothing small enough
        self.assertEqual((found, visited), ([], 1))
        self.assertEqual(sol.report_at_most(ex.FibHeap([5]), 5)[0], [(5, None)])
        h = ex.FibHeap(ex.BRANCH_A + ex.BRANCH_B)
        self.assertEqual(sorted(k for k, _ in sol.report_at_most(h, 50)[0]), [12, 25, 31, 47])
        for seed in range(20):
            rng = random.Random(seed)
            h = ex.FibHeap()
            nodes = [h.insert(rng.randrange(1000), i) for i in range(rng.randrange(1, 400))]
            if len(h) > 1:
                h.delete_min()
            for x in rng.sample(nodes, len(nodes) // 3):
                if x.parent is not None or x in h.roots:
                    h.decrease_key(x, x.key - rng.randrange(100))
            bound = rng.randrange(-50, 1000)
            before = sorted(x.key for x in h.nodes())
            found, visited = sol.report_at_most(h, bound)
            self.assertEqual(sorted(k for k, _ in found), [k for k in before if k <= bound])
            self.assertEqual(sorted(x.key for x in h.nodes()), before)    # nothing removed
            self.assertTrue(h.valid())
            d = ex.degree_bound(len(h))
            self.assertLessEqual(visited, (len(found) + 1) * (d + 1))

    def test_no_cascade_breaks_degree_bound(self) -> None:
        deg, size, n, h = sol.star(sol.NoCascadeFibHeap, 4)
        self.assertEqual((deg, size, n), (4, 5, 5))
        self.assertLess(size, ex.fib(deg + 2))
        self.assertFalse(h.valid())
        deg, size, n, h = sol.star(sol.NoCascadeFibHeap, 10)
        self.assertEqual((deg, n, ex.degree_bound(n)), (10, 11, 4))
        for d in (1, 2, 3, 4, 6):
            deg, size, n, h = sol.star(ex.FibHeap, d)                   # with cascading cuts: always fine
            self.assertTrue(h.valid())
            self.assertLessEqual(h.max_degree(), ex.degree_bound(n))
        deg, size, n, h = sol.star(sol.NoCascadeFibHeap, 1)              # smallest input: nothing to delete
        self.assertEqual((deg, size, n), (1, 2, 2))


if __name__ == "__main__":
    unittest.main()
