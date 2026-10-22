import itertools
import math
import random
import unittest

import ch12_solutions as sol
from ch12_solutions import avl
import ch09_examples as bt


class TestChapter12Solutions(unittest.TestCase):
    def test_b_tree_never_taller_than_a_binary_tree(self) -> None:
        rng = random.Random(4)
        for _ in range(200):
            n = rng.randint(1, 3000)
            keys = rng.sample(range(10 ** 5), n)
            shortest_binary = math.ceil(math.log2(n + 1)) - 1
            for max_keys in (3, 5, 63):
                self.assertLessEqual(bt.BTree(max_keys, keys).height(), shortest_binary)

    def test_merge(self) -> None:
        self.assertIsNone(sol.merge_avl(None, None))                       # both empty
        one = sol.merge_avl(avl.build([5]), None)
        self.assertEqual(avl.shape(one), (5, None, None))
        self.assertEqual(avl.inorder(sol.merge_avl(avl.build([5]), avl.build([5]))), [5])   # shared key
        self.assertEqual(avl.inorder(sol.merge_avl(avl.build([1]), avl.build([2]))), [1, 2])
        rng = random.Random(7)
        for _ in range(300):
            a = rng.sample(range(200), rng.randint(0, 60))
            b = rng.sample(range(200), rng.randint(0, 60))
            m = sol.merge_avl(avl.build(a), avl.build(b))
            keys = sorted(set(a) | set(b))
            self.assertEqual(avl.inorder(m), keys)
            self.assertTrue(avl.is_avl(m))
            self.assertEqual(avl.h(m), len(keys).bit_length() - 1)        # the smallest possible height

    def test_avl_can_be_taller_than_red_black(self) -> None:
        self.assertEqual(sol.heights(sol.AVL_TALLER), (4, 3))
        for n in range(1, 8):                                              # never with fewer keys (see the text)
            for p in itertools.permutations(range(n)):
                a, r = sol.heights(p)
                self.assertLessEqual(a, r)


if __name__ == "__main__":
    unittest.main()
