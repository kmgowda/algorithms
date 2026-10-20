import random
import unittest

import ch45_examples as ex


class TestChapter45(unittest.TestCase):
    def test_against_sorted_set(self) -> None:
        rng = random.Random(1)
        for _ in range(100):
            t, ref = ex.BST(), set()
            for _ in range(80):
                k = rng.randint(0, 40)
                if rng.random() < 0.6:
                    t.insert(k); ref.add(k)
                else:
                    t.delete(k); ref.discard(k)
                self.assertEqual(t.inorder(), sorted(ref))
            a, b = sorted(rng.sample(range(41), 2))
            self.assertEqual(t.range(a, b), [k for k in sorted(ref) if a <= k <= b])

    def test_examples(self) -> None:
        t = ex.BST(ex.ORDER)
        self.assertEqual(t.search_path(63), [58, 84, 70, 63])
        self.assertEqual(t.search_path(65), [58, 84, 70, 63])
        self.assertFalse(t.contains(65))
        self.assertEqual(t.range(30, 70), [31, 47, 58, 63, 70])
        t.insert(40)
        self.assertEqual(t.search_path(40), [58, 25, 47, 31, 40])
        t2 = ex.BST(ex.ORDER)
        t2.delete(25)
        self.assertEqual(t2.root.left.key, 31)
        t2.delete(84)
        self.assertEqual(t2.root.right.key, 91)
        self.assertEqual(ex.BST([50, 30, 70, 20, 40, 60, 80]).height(), 2)


if __name__ == "__main__":
    unittest.main()
