import random
import unittest

import ch16_examples as ex


class TestChapter45(unittest.TestCase):
    def test_every_case(self) -> None:
        keys = [58, 25, 84, 12, 47, 70, 91]
        t = ex.BST(keys); t.delete(12)
        self.assertEqual(t.inorder(), [25, 47, 58, 70, 84, 91])
        t.delete(25)
        self.assertEqual(t.inorder(), [47, 58, 70, 84, 91])
        t = ex.BST(keys); t.delete(58)
        self.assertEqual((t.inorder(), t.root.key), ([12, 25, 47, 70, 84, 91], 70))
        t = ex.BST(keys); t.delete(99)
        self.assertEqual(t.inorder(), sorted(keys))
        t = ex.BST([5]); t.delete(5)
        self.assertIsNone(t.root)
        t = ex.BST(); t.delete(3)
        self.assertEqual((t.inorder(), t.contains(3), t.search_path(3)), ([], False, []))
        self.assertEqual(ex.BST([5, 5, 5]).inorder(), [5])
        self.assertEqual((ex.BST([58, 25, 84]).range(30, 60), ex.BST([58, 25, 84]).range(60, 30)), ([58], []))

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
