import math
import random
import unittest

import ch04_examples as ex
import ch04_solutions as sol

N = ex.Node


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return None
    return N(rng.randint(-20, 20), random_tree(rng, depth - 1), random_tree(rng, depth - 1))


def brute_max_path(root):
    """Try every pair of nodes as the two ends of a path."""
    nodes, parent = [], {}

    def walk(n, p):
        if n:
            nodes.append(n)
            parent[id(n)] = p
            walk(n.left, n)
            walk(n.right, n)
    walk(root, None)

    def up(n):
        out = []
        while n is not None:
            out.append(n)
            n = parent[id(n)]
        return out
    best = -math.inf
    for a in nodes:
        for b in nodes:
            pa, pb = up(a), up(b)
            ids_b = {id(x) for x in pb}
            top = next(x for x in pa if id(x) in ids_b)
            total = sum(x.value for x in pa[:pa.index(top) + 1]) + sum(x.value for x in pb[:pb.index(top)])
            best = max(best, total)
    return best


def full_tree(rng, n):
    if n == 1:
        return N(0)
    k = rng.randrange(1, n - 1, 2)          # odd sizes on each side
    return N(0, full_tree(rng, k), full_tree(rng, n - 1 - k))


class TestChapter04Solutions(unittest.TestCase):
    def test_max_path_small(self) -> None:
        self.assertEqual(sol.max_path_sum(None), -math.inf)
        self.assertEqual(sol.max_path_sum(N(-4)), -4)
        self.assertEqual(sol.max_path_sum(N(-3, N(-7), N(-1))), -1)
        self.assertEqual(sol.max_path_sum(N(1, N(2), N(3))), 6)
        self.assertEqual(sol.max_path_sum(ex.library()), 59)              # Mystery up to Library, down to Algebra
        self.assertEqual(sol.max_path_sum(N(10, N(-5, N(30), N(40)))), 65)   # the path bends below the root

    def test_max_path_random(self) -> None:
        rng = random.Random(7)
        for _ in range(300):
            t = random_tree(rng, 5)
            self.assertEqual(sol.max_path_sum(t), brute_max_path(t))

    def test_lca_shortcut_bug(self) -> None:
        t = None
        for k in [50, 30, 70, 20, 40, 60, 80, 35]:
            node = N(k)
            if t is None:
                t = node
                continue
            n = t
            while True:
                side = "left" if k < n.value else "right"
                if getattr(n, side) is None:
                    setattr(n, side, node)
                    break
                n = getattr(n, side)
        self.assertEqual(sol.lca_shortcut(t, 35, 20).value, 30)          # fine when both are present
        self.assertEqual(sol.lca_shortcut(t, 35, 99).value, 35)          # wrong: 99 is not in the tree
        self.assertIsNone(ex.lowest_common_ancestor(t, 35, 99))
        self.assertIsNone(sol.lca_shortcut(None, 1, 2))

    def test_min_depth_bound(self) -> None:
        self.assertEqual([sol.min_depth_bound(n) for n in (1, 3, 7, 9, 15)], [0, 1, 2, 2, 3])
        self.assertEqual(ex.min_depth(ex.library()), sol.min_depth_bound(9))     # Figure 4.1: tight
        rng = random.Random(2)
        for _ in range(300):
            n = rng.randrange(1, 60, 2)
            self.assertLessEqual(ex.min_depth(full_tree(rng, n)), sol.min_depth_bound(n))
        chain = N(1, N(2, N(3, N(4))))                                     # not full: the bound fails
        self.assertGreater(ex.min_depth(chain), sol.min_depth_bound(4))


if __name__ == "__main__":
    unittest.main()
