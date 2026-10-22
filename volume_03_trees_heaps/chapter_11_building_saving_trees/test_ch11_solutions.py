import random
import unittest

import ch11_examples as ex
import ch11_solutions as sol


def random_tree(rng, keys, full=False):
    if not keys:
        return None
    if full and len(keys) % 2 == 0:
        keys = keys[:-1]
    if full:
        if len(keys) == 1:
            return ex.Node(keys[0])
        k = rng.randrange(0, len(keys) - 1, 2) + 1          # odd sizes on both sides keep the tree full
        return ex.Node(keys[k], random_tree(rng, keys[:k], True), random_tree(rng, keys[k + 1:], True))
    k = rng.randrange(len(keys))
    return ex.Node(keys[k], random_tree(rng, keys[:k]), random_tree(rng, keys[k + 1:]))


def postorder(n):
    return [] if n is None else postorder(n.left) + postorder(n.right) + [n.value]


class TestChapter11Solutions(unittest.TestCase):
    def test_full_tree_from_pre_post(self) -> None:
        self.assertIsNone(sol.from_pre_post_full([], []))
        self.assertEqual(ex.save(sol.from_pre_post_full([7], [7])), "7 # #")
        self.assertEqual(ex.save(sol.from_pre_post_full([1, 2, 4, 5, 3], [4, 5, 2, 3, 1])), "1 2 4 # # 5 # # 3 # #")
        rng = random.Random(1)
        for _ in range(300):
            t = random_tree(rng, list(range(rng.randrange(0, 40))), full=True)
            self.assertEqual(ex.save(sol.from_pre_post_full(ex.preorder(t), postorder(t))), ex.save(t))

    def test_bst_from_preorder(self) -> None:
        self.assertIsNone(sol.bst_from_preorder([]))
        self.assertEqual(ex.save(sol.bst_from_preorder([5])), "5 # #")
        self.assertEqual(ex.save(sol.bst_from_preorder([8, 3, 1, 6, 10, 14])), "8 3 1 # # 6 # # 10 # 14 # #")
        self.assertEqual(ex.save(sol.bst_from_preorder([3, 2, 1])), "3 2 1 # # # #")         # a left chain
        self.assertEqual(ex.save(sol.bst_from_preorder([1, 2, 3])), "1 # 2 # 3 # #")         # a right chain
        with self.assertRaises(ValueError):
            sol.bst_from_preorder([5, 8, 6, 3])            # 3 comes after the right subtree began
        with self.assertRaises(ValueError):
            sol.bst_from_preorder([5, 5])                  # a repeated key
        rng = random.Random(2)
        for _ in range(300):
            t = random_tree(rng, sorted(rng.sample(range(1000), rng.randrange(0, 60))))
            self.assertEqual(ex.save(sol.bst_from_preorder(ex.preorder(t))), ex.save(t))

    def test_count_only_is_wrong(self) -> None:
        for line in ("# 5 #", "5 # # # 7", "# # 5"):
            self.assertTrue(sol.count_only(line))
            self.assertFalse(ex.complete(line))
        for line in ("#", "5 # #", "58 25 12 # # 47 # # 84 # 91 # #"):
            self.assertTrue(sol.count_only(line) and ex.complete(line))


if __name__ == "__main__":
    unittest.main()
