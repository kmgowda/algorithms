import random
import unittest

import ch05_examples as ex


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
        self.assertEqual((ex.BST(keys).range(30, 60), ex.BST(keys).range(60, 30)), ([47, 58], []))

    def test_predecessor_floor_ceiling_lca(self) -> None:
        t = ex.BST(ex.ORDER); t.delete(25, use_predecessor=True)
        self.assertEqual((t.root.left.key, t.root.left.left, t.root.left.right.key), (12, None, 47))
        self.assertEqual(t.inorder(), [12, 31, 47, 58, 63, 70, 84, 91])
        t = ex.BST(ex.ORDER); t.delete(58, use_predecessor=True)
        self.assertEqual(t.root.key, 47)
        p = ex.BST([50, 30, 70, 20, 40, 60, 80, 35])                                  # practice problems
        self.assertEqual((p.floor(45), p.ceiling(45), p.floor(85), p.ceiling(85)), (40, 50, 80, None))
        self.assertEqual((p.lowest_common_ancestor(20, 35), p.lowest_common_ancestor(60, 80)), (30, 70))
        q = ex.BST([50, 30, 70, 20, 40, 60, 80, 35]); q.delete(30)
        r = ex.BST([50, 30, 70, 20, 40, 60, 80, 35]); r.delete(30, use_predecessor=True)
        self.assertEqual((q.root.left.key, r.root.left.key), (35, 20))
        t = ex.BST(ex.ORDER)
        self.assertEqual((t.floor(60), t.ceiling(60), t.floor(58), t.ceiling(58)), (58, 63, 58, 58))
        self.assertEqual((t.floor(10), t.ceiling(95), t.floor(95), t.ceiling(10)), (None, None, 91, 12))
        self.assertEqual((ex.BST().floor(5), ex.BST().ceiling(5), ex.BST().successor(5)), (None, None, None))
        self.assertEqual((t.successor(47), t.successor(31), t.successor(91), t.successor(60)), (58, 47, None, 63))
        self.assertEqual((t.lowest_common_ancestor(31, 12), t.lowest_common_ancestor(31, 63),
                          t.lowest_common_ancestor(63, 91), t.lowest_common_ancestor(47, 47),
                          t.lowest_common_ancestor(31, 99), ex.BST().lowest_common_ancestor(1, 2)),
                         (25, 58, 84, 47, None, None))
        rng = random.Random(2)
        for _ in range(200):
            keys = rng.sample(range(100), rng.randint(0, 30))
            t, q = ex.BST(keys), rng.randint(-5, 105)
            below, above = [k for k in keys if k <= q], [k for k in keys if k >= q]
            self.assertEqual(t.floor(q), max(below) if below else None)
            self.assertEqual(t.ceiling(q), min(above) if above else None)
            nxt = [k for k in keys if k > q]
            self.assertEqual(t.successor(q), min(nxt) if nxt else None)
            t2 = ex.BST(keys); ref = sorted(set(keys))
            for k in keys[:5]:
                t2.delete(k, use_predecessor=True); ref.remove(k)
                self.assertEqual(t2.inorder(), ref)

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
