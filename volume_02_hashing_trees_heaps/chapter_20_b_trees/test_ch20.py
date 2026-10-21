import random
import unittest

import ch20_examples as ex


class TestChapter49(unittest.TestCase):
    def test_every_case(self) -> None:
        B = ex.BTree
        rows = [([], [[[]]], 0, 0), ([5], [[[5]]], 0, 0), ([1, 2, 3], [[[1, 2, 3]]], 0, 0),
                ([1, 2, 3, 4], [[[2]], [[1], [3, 4]]], 1, 1), ([1, 2, 3, 4, 5, 6, 7], [[[2, 4]], [[1], [3], [5, 6, 7]]], 1, 2),
                ([5, 5], [[[5]]], 0, 0)]
        for keys, levels, h, splits in rows:
            t = B(3, keys)
            self.assertEqual((t.levels(), t.height(), t.splits), (levels, h, splits))
        big = B(3, range(1, 101))
        self.assertEqual((big.height(), big.splits, big.leaves_same_depth()), (5, 90, True))
        t = B(3, [10, 20, 30, 40, 50])
        self.assertEqual((t.search(30), t.search(35), t.search(5), B(3).search(1)), ((True, 2), (False, 2), (False, 2), (False, 1)))

    def test_btree(self) -> None:
        t = ex.BTree(3, [58, 25, 84, 12, 47, 70, 91, 31, 63])
        self.assertEqual(t.levels(), [[[25, 58, 84]], [[12], [31, 47], [63, 70], [91]]])
        self.assertEqual(t.search(63), (True, 2))
        t.insert(95)
        self.assertEqual(t.levels()[0], [[58]])
        self.assertEqual(ex.BTree(199, range(100_000)).height(), 2)
        rng = random.Random(1)
        for m in (3, 5, 7):
            for _ in range(40):
                keys = [rng.randint(0, 500) for _ in range(rng.randint(1, 120))]
                b = ex.BTree(m, keys)
                self.assertEqual(b.inorder(), sorted(set(keys)))
                self.assertTrue(b.leaves_same_depth())
                for k in keys[:10]:
                    self.assertTrue(b.search(k)[0])


if __name__ == "__main__":
    unittest.main()
