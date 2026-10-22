import random
import unittest

import ch27_examples as ex
import ch27_solutions as sol


class TestKNearest(unittest.TestCase):
    def test_small(self) -> None:
        t = ex.kd.KDTree([])
        self.assertEqual(sol.k_nearest(t, (1, 1), 3), [])
        t = ex.kd.KDTree(ex.kd.BRANCHES.values())
        self.assertEqual(sol.k_nearest(t, ex.kd.READER, 0), [])
        self.assertEqual(sol.k_nearest(t, ex.kd.READER, 1), [(2, (8, 5))])
        self.assertEqual([ex.kd.NAME[p] for _, p in sol.k_nearest(t, ex.kd.READER, 3)],
                         ["Wharf", "Market", "Riverside"])
        self.assertEqual(len(sol.k_nearest(t, ex.kd.READER, 20)), 9)

    def test_random(self) -> None:
        rng = random.Random(27)
        for n in (1, 2, 5, 50, 500):
            pts = [(rng.randrange(100), rng.randrange(100)) for _ in range(n)]
            t = ex.kd.KDTree(pts)
            for _ in range(20):
                q, k = (rng.randrange(100), rng.randrange(100)), rng.randrange(0, 8)
                got = [d for d, _ in sol.k_nearest(t, q, k)]
                want = [d for d, _ in sol.brute_k_nearest(pts, q, k)]
                self.assertEqual(got, want)

    def test_visits(self) -> None:
        t = ex.kd.KDTree(ex.kd.random_points(10_000, 2, 1))
        rng = random.Random(2)
        for k in (1, 10):
            t.visited = 0
            for _ in range(100):
                sol.k_nearest(t, (rng.random(), rng.random()), k)
            self.assertLess(t.visited / 100, 200)


class TestTreapVersusRoot(unittest.TestCase):
    def test_numbers(self) -> None:
        root, k, treap, bound = sol.treap_versus_root()
        self.assertEqual(k, root + 1)
        self.assertGreater(treap, 15)
        self.assertLess(treap, bound)


if __name__ == "__main__":
    unittest.main()
