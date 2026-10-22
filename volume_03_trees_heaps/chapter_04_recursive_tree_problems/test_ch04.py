import random
import unittest

import ch04_examples as ex


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.25:
        return None
    return ex.Node(rng.randint(0, 50), random_tree(rng, depth - 1), random_tree(rng, depth - 1))


def values(n):
    return [] if n is None else [n.value] + values(n.left) + values(n.right)


def search_tree(keys):
    root = None
    for k in keys:
        if root is None:
            root = ex.Node(k)
            continue
        n = root
        while True:
            side = "left" if k < n.value else "right"
            if getattr(n, side) is None:
                setattr(n, side, ex.Node(k))
                break
            n = getattr(n, side)
    return root


class TestChapter44(unittest.TestCase):
    def test_every_case(self) -> None:
        N, L = ex.Node, ex.library()
        self.assertEqual((ex.size(None), ex.total(None), ex.height(None), ex.largest(None)), (0, 0, -1, float("-inf")))
        self.assertTrue(ex.same_tree(None, None) and ex.symmetric(None))
        self.assertEqual((ex.size(L), ex.total(L), ex.height(L), ex.largest(L), ex.best_walk(L)), (9, 108, 3, 30, 37))
        self.assertEqual((ex.best_walk(N(7)), ex.symmetric(N(7))), (7, True))
        self.assertFalse(ex.same_tree(N(1), None))
        self.assertFalse(ex.same_tree(N(1, N(2)), N(1, None, N(2))))
        self.assertEqual((ex.largest(N(-5, N(-9))), ex.best_walk(N(1, N(-10), N(-2)))), (-5, -1))
        with self.assertRaises(AttributeError):
            ex.best_walk(None)

    def test_min_depth_and_lca(self) -> None:
        N, L = ex.Node, ex.library()
        self.assertEqual((ex.min_depth(None), ex.min_depth(N(7)), ex.min_depth(L)), (-1, 0, 2))
        self.assertEqual(ex.min_depth(N(50, None, N(70, None, N(80)))), 2)    # the one-child trap
        t = search_tree([50, 30, 70, 20, 40, 60, 80, 35])
        lca = lambda a, b: (lambda n: n.value if n else None)(ex.lowest_common_ancestor(t, a, b))
        self.assertEqual((lca(35, 20), lca(35, 60), lca(40, 35), lca(80, 80), lca(35, 99)), (30, 50, 40, 80, None))
        self.assertEqual((lca(20, 40), lca(35, 80), lca(35, 30), ex.min_depth(t)), (30, 50, 30, 2))  # practice
        self.assertIsNone(ex.lowest_common_ancestor(None, 1, 2))
        self.assertEqual(ex.lowest_common_ancestor(L, 12, 18).value, 4)        # Algebra and Physics: Science

    def test_library(self) -> None:
        lib = ex.library()
        self.assertEqual((ex.size(lib), ex.total(lib), ex.height(lib), ex.best_walk(lib)), (9, 108, 3, 37))
        lib.right.right.left.value = 40
        self.assertEqual(ex.best_walk(lib), 52)

    def test_random(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            t = random_tree(rng, 6)
            v = values(t)
            self.assertEqual(ex.size(t), len(v))
            self.assertEqual(ex.total(t), sum(v))
            if v:
                self.assertEqual(ex.largest(t), max(v))
            self.assertTrue(ex.same_tree(t, ex.mirror(ex.mirror(t))))
        self.assertTrue(ex.symmetric(ex.Node(1, ex.Node(2, ex.Node(3), ex.Node(4)), ex.Node(2, ex.Node(4), ex.Node(3)))))
        self.assertFalse(ex.symmetric(ex.Node(1, ex.Node(2), ex.Node(3))))

    def test_paths_with_total(self) -> None:
        t = search_tree([50, 30, 70, 20, 40, 60, 80, 35])          # Section 4.15: totals 100, 155, 180, 200
        self.assertEqual([ex.paths_with_total(t, s) for s in (100, 155, 180, 200, 150)], [1, 1, 1, 1, 0])
        self.assertEqual((ex.paths_with_total(None, 0), ex.paths_with_total(ex.Node(7), 7)), (0, 1))


if __name__ == "__main__":
    unittest.main()
