import random
import unittest

import ch03_examples as ex
import ch03_solutions as sol

T = ex.TreeNode


def random_tree(rng, depth):
    if depth == 0 or rng.random() < 0.3:
        return None
    return T(rng.randint(0, 99), random_tree(rng, depth - 1), random_tree(rng, depth - 1))


def shape(n):
    return None if n is None else (n.value, shape(n.left), shape(n.right))


class TestChapter03Solutions(unittest.TestCase):
    def test_small(self) -> None:
        self.assertEqual((sol.morris_inorder(None), sol.postorder_by_reversal(None)), ([], []))
        self.assertEqual((sol.morris_inorder(T(5)), sol.postorder_by_reversal(T(5))), ([5], [5]))
        left = T(3, T(2, T(1)))
        right = T(1, None, T(2, None, T(3)))
        self.assertEqual((sol.morris_inorder(left), sol.morris_inorder(right)), ([1, 2, 3], [1, 2, 3]))

    def test_morris_matches_and_restores(self) -> None:
        rng = random.Random(3)
        for _ in range(300):
            t = random_tree(rng, 7)
            before = shape(t)
            self.assertEqual(sol.morris_inorder(t), ex.inorder(t))
            self.assertEqual(shape(t), before)                       # every thread was removed
        t = ex.from_array([58, 25, 84, 12, 47, 70, 91])
        self.assertEqual(sol.morris_inorder(t), [12, 25, 47, 58, 70, 84, 91])

    def test_deep_chain(self) -> None:
        root = T(0)
        n = root
        for v in range(1, 5000):
            n.left = T(v)
            n = n.left
        self.assertEqual(sol.morris_inorder(root), list(range(4999, -1, -1)))
        self.assertEqual(len(sol.postorder_by_reversal(root)), 5000)

    def test_reversed_preorder_is_not_postorder(self) -> None:
        t = T(2, T(1), T(3))
        self.assertEqual(ex.preorder(t)[::-1], [3, 1, 2])
        self.assertEqual(ex.postorder(t), [1, 3, 2])
        t = ex.from_array([58, 25, 84, 12, 47, 70, 91])
        self.assertEqual(ex.preorder(t)[::-1], [91, 70, 84, 47, 12, 25, 58])
        rng = random.Random(4)
        for _ in range(300):
            t = random_tree(rng, 7)
            self.assertEqual(sol.postorder_by_reversal(t), ex.postorder(t))

    def test_pre_and_post_do_not_decide(self) -> None:
        a, b = T(1, T(2)), T(1, None, T(2))                         # Thinking Problem 1
        self.assertEqual((ex.preorder(a), ex.postorder(a)), (ex.preorder(b), ex.postorder(b)))
        self.assertNotEqual(ex.inorder(a), ex.inorder(b))


if __name__ == "__main__":
    unittest.main()
