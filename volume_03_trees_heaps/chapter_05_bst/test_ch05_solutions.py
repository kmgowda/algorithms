import itertools
import random
import unittest

import ch05_examples as ex
import ch05_solutions as sol


def brute_pairs(keys, target):
    return {(a, b) for a, b in itertools.combinations(sorted(set(keys)), 2) if a + b == target}


class TestChapter05Solutions(unittest.TestCase):
    def test_pair_small(self) -> None:
        self.assertIsNone(sol.pair_with_sum(ex.BST(), 10))
        self.assertIsNone(sol.pair_with_sum(ex.BST([5]), 10))          # one key cannot be used twice
        self.assertEqual(sol.pair_with_sum(ex.BST([5, 3]), 8), (3, 5))
        self.assertIsNone(sol.pair_with_sum(ex.BST([5, 3]), 9))

    def test_pair_shelf(self) -> None:
        shelf = ex.BST(ex.ORDER)
        self.assertEqual(sol.pair_with_sum(shelf, 116), (25, 91))
        self.assertEqual(sol.pair_with_sum(shelf, 133), (63, 70))        # the traced example
        self.assertIsNone(sol.pair_with_sum(shelf, 100))
        self.assertEqual(sol.pair_with_sum(shelf, 24), None)              # 12 + 12 is not allowed

    def test_pair_random(self) -> None:
        rng = random.Random(9)
        for _ in range(400):
            keys = rng.sample(range(60), rng.randrange(0, 15))
            t = rng.randrange(0, 120)
            got = sol.pair_with_sum(ex.BST(keys), t)
            want = brute_pairs(keys, t)
            if want:
                self.assertIn(got, want)
            else:
                self.assertIsNone(got)
        chain = ex.BST(range(3000))                                       # degenerate tree, no recursion
        self.assertEqual(sol.pair_with_sum(chain, 5997), (2998, 2999))

    def test_buggy_delete(self) -> None:
        t = ex.BST(ex.ORDER + [40])
        sol.buggy_delete(t, 25)
        self.assertNotIn(40, t.inorder())                                 # 40 was lost with the old 31
        self.assertEqual(t.inorder(), [12, 31, 47, 58, 63, 70, 84, 91])
        good = ex.BST(ex.ORDER + [40])
        good.delete(25)
        self.assertEqual(good.inorder(), [12, 31, 40, 47, 58, 63, 70, 84, 91])

    def test_delete_does_not_commute(self) -> None:
        a, b = ex.BST([25, 12, 47, 31]), ex.BST([25, 12, 47, 31])
        a.delete(12)
        a.delete(25)
        b.delete(25)
        b.delete(12)
        self.assertEqual(sol.shape(a), (47, (31, None, None), None))
        self.assertEqual(sol.shape(b), (31, None, (47, None, None)))
        self.assertEqual(a.inorder(), b.inorder())


if __name__ == "__main__":
    unittest.main()
