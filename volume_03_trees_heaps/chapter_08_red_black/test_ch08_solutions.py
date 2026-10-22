import random
import unittest

import ch08_examples as ex
import ch08_solutions as sol
from ch08_solutions import avl


class TestChapter8Solutions(unittest.TestCase):
    def test_every_avl_tree_can_be_coloured(self) -> None:
        self.assertIsNone(sol.colour_avl(None).root)                  # the empty tree
        self.assertEqual(sol.colour_avl(avl.build([5])).shape(), ((5, "B"), None, None))
        for hh in range(0, 12):                                       # the sparsest, most lopsided AVL trees
            t = sol.colour_avl(avl.sparsest(hh))
            self.assertTrue(t.valid())
            self.assertEqual(t.height(), hh)
        rng = random.Random(3)
        for _ in range(300):
            keys = rng.sample(range(1000), rng.randint(0, 150))
            t = sol.colour_avl(avl.build(keys))
            self.assertTrue(t.valid())
            self.assertEqual(t.inorder(), sorted(keys))

    def test_rb_from_sorted(self) -> None:
        self.assertIsNone(sol.rb_from_sorted([]).root)
        self.assertEqual(sol.rb_from_sorted([7]).shape(), ((7, "B"), None, None))
        self.assertEqual(sol.rb_from_sorted([1, 2]).shape(), ((1, "B"), None, ((2, "R"), None, None)))
        for n in range(0, 300):
            keys = list(range(0, 3 * n, 3))
            t = sol.rb_from_sorted(keys)
            self.assertTrue(t.valid())
            self.assertEqual(t.inorder(), keys)
            self.assertEqual(t.height(), n.bit_length() - 1)
        t = sol.rb_from_sorted([12, 25, 31, 47, 58, 63, 70, 84, 91])
        t.insert(50)                                                  # still a working red-black tree
        t.delete(58)
        self.assertTrue(t.valid())

    def test_skipping_case_3_breaks_rule_4(self) -> None:
        bad = sol.SkipCase3Tree([12, 25, 31, 47, 58, 63, 70])
        bad.delete(70)
        bad.delete(31)
        self.assertEqual(bad.shape(), ((25, "B"), ((12, "B"), None, None),
                                       ((63, "R"), ((47, "B"), None, ((58, "R"), None, None)), None)))
        self.assertFalse(bad.valid())
        good = ex.RedBlackTree([12, 25, 31, 47, 58, 63, 70])
        good.delete(70)
        good.delete(31)
        self.assertTrue(good.valid())


if __name__ == "__main__":
    unittest.main()
