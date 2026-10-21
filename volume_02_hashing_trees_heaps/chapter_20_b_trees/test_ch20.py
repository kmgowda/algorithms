import random
import unittest

import ch20_examples as ex


class TestChapter49(unittest.TestCase):
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
