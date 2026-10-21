import random
import unittest

import ch19_examples as ex


class TestChapter48(unittest.TestCase):
    def test_red_black(self) -> None:
        t = ex.RedBlackTree([12, 25, 31, 47, 58, 63, 70])
        self.assertEqual(t.shape()[0], (25, "B"))
        self.assertTrue(t.valid())
        t2 = ex.RedBlackTree([20, 10, 30])
        t2.insert(5)
        self.assertEqual(t2.shape(), ((20, "B"), ((10, "B"), ((5, "R"), None, None), None), ((30, "B"), None, None)))
        big = ex.RedBlackTree(range(1000))
        self.assertTrue(big.valid())
        self.assertEqual(big.height(), 16)
        rng = random.Random(1)
        for _ in range(100):
            keys = [rng.randint(0, 300) for _ in range(rng.randint(1, 80))]
            t = ex.RedBlackTree()
            for k in keys:
                t.insert(k)
                self.assertTrue(t.valid())
            self.assertEqual(t.inorder(), sorted(set(keys)))


if __name__ == "__main__":
    unittest.main()
