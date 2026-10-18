import random
import unittest

import ch02_examples as ex
import ch02_solutions as sol


def random_tree(rng, n):
    values = list(range(n))
    rng.shuffle(values)
    root = None
    for v in values:                      # random shapes by random descents
        if root is None:
            root = ex.Node(v)
            continue
        node = root
        while True:
            side = rng.choice(("left", "right"))
            child = getattr(node, side)
            if child is None:
                setattr(node, side, ex.Node(v))
                break
            node = child
    return root


class TestBinaryTrees(unittest.TestCase):
    def test_example(self) -> None:
        t = ex.from_level_list(["lion", "tiger", "zebra", "puma", None, "horse", "okapi"])
        self.assertEqual((ex.size(t), ex.height(t), ex.count_leaves(t)), (6, 2, 3))
        self.assertEqual(ex.depth_of(t, "okapi"), 2)
        self.assertEqual(ex.depth_of(t, "cat"), -1)
        self.assertFalse(ex.is_full(t))
        self.assertFalse(ex.is_complete(t))
        self.assertFalse(ex.is_perfect(t))

    def test_shapes(self) -> None:
        self.assertTrue(ex.is_perfect(ex.from_level_list([1, 2, 3, 4, 5, 6, 7])))
        self.assertTrue(ex.is_complete(ex.from_level_list([1, 2, 3, 4, 5])))
        self.assertFalse(ex.is_complete(ex.from_level_list([1, 2, 3, None, 5])))
        self.assertTrue(ex.is_full(ex.from_level_list([1, 2, 3, 4, 5])))
        self.assertEqual(ex.height(None), -1)
        self.assertIsNone(ex.from_level_list([]))

    def test_random_bounds(self) -> None:
        rng = random.Random(1)
        for _ in range(200):
            n = rng.randint(1, 40)
            t = random_tree(rng, n)
            self.assertEqual(ex.size(t), n)
            self.assertTrue(sol.min_height(n) <= ex.height(t) <= n - 1)
            self.assertLessEqual(n, sol.max_nodes(ex.height(t)))

    def test_decide(self) -> None:
        loan = ex.Node("income?", ex.Node("reject"), ex.Node("credit?", ex.Node("review"), ex.Node("approve")))
        self.assertEqual(ex.decide(loan, {"income?": False}), "reject")
        self.assertEqual(ex.decide(loan, {"income?": True, "credit?": True}), "approve")


class TestSolutions(unittest.TestCase):
    def test_solutions(self) -> None:
        a, b = ex.from_level_list([1, 2, 3, 4]), ex.from_level_list([1, 2, 3, 4])
        self.assertTrue(sol.same_tree(a, b))
        sol.mirror(b)
        self.assertFalse(sol.same_tree(a, b))
        sol.mirror(b)
        self.assertTrue(sol.same_tree(a, b))
        self.assertEqual(sol.max_nodes(3), 15)
        self.assertEqual([sol.min_height(n) for n in (1, 2, 3, 4, 10)], [0, 1, 1, 2, 3])
        self.assertEqual(sol.sum_values(ex.from_level_list([1, 2, 3])), 6)


if __name__ == "__main__":
    unittest.main()
