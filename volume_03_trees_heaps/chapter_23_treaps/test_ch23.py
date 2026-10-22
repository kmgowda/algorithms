import random
import unittest

import ch23_examples as ex


class TestChapter23(unittest.TestCase):
    def test_every_case(self) -> None:
        t = ex.Treap(priorities=ex.ROLLS)
        self.assertFalse(t.contains(47))                    # empty treap
        self.assertFalse(t.delete(47))
        self.assertEqual(ex.split(None, 40), (None, None))
        self.assertIsNone(ex.merge(None, None))
        self.assertTrue(t.insert(47))                        # one key: it is the root, no rotation
        self.assertEqual((t.shape(prio=True), t.last_rotations), (((47, 63), None, None), 0))
        self.assertFalse(t.insert(47))                       # duplicate refused, tree unchanged
        self.assertEqual(t.keys(), [47])
        t.insert(31)                                         # 18 < 63: a leaf, no rotation
        self.assertEqual(t.last_rotations, 0)
        t.insert(25)                                         # 77 beats 18 and 63: two rotations
        self.assertEqual((t.last_rotations, t.shape()), (2, (25, None, (47, (31, None, None), None))))
        t = ex.shelf_treap()
        self.assertTrue(t.delete(91))                        # a leaf: cut off, no rotation
        self.assertEqual(t.last_rotations, 0)
        t = ex.shelf_treap()
        self.assertTrue(t.delete(25))                        # inner node: rotated down twice
        self.assertEqual(t.last_rotations, 2)
        t = ex.shelf_treap()
        self.assertTrue(t.delete(58))                        # the root: three rotations
        self.assertEqual(t.last_rotations, 3)
        self.assertTrue(t.valid())
        t = ex.Treap([5], priorities={5: 1})
        self.assertTrue(t.delete(5))                         # the only key
        self.assertIsNone(t.root)
        for key, left, right in ((58, [12, 25, 31, 47], [58, 63, 70, 84, 91]),     # a key present goes right
                                 (40, [12, 25, 31], [47, 58, 63, 70, 84, 91]),     # absent
                                 (5, [], ex.SHELF), (99, ex.SHELF, [])):            # beyond the ends
            a, b = ex.split(ex.shelf_treap().root, key)
            self.assertEqual((ex.from_root(a).keys(), ex.from_root(b).keys()), (left, right))
            self.assertTrue(ex.is_treap(a) and ex.is_treap(b))
        r = ex.shelf_treap().root
        self.assertIs(ex.merge(r, None), r)                   # merge with an empty treap
        self.assertIs(ex.merge(None, r), r)

    def test_shelf_and_uniqueness(self) -> None:
        t = ex.shelf_treap()
        expected = (58, (25, (12, None, None), (47, (31, None, None), None)),
                    (70, (63, None, None), (84, None, (91, None, None))))
        self.assertEqual((t.shape(), t.height(), t.rotations), (expected, 3, 5))
        self.assertEqual(ex.shelf_treap(ex.RETURNS).shape(), expected)
        self.assertEqual(ex.priority_order_bst(ex.ROLLS), expected)
        self.assertEqual(ex.plain_bst_shape(ex.SHELF)[2][2][2][2][2][2][2][2], (91, None, None))
        rng = random.Random(5)
        for _ in range(200):
            keys = rng.sample(range(100), rng.randrange(1, 30))
            prios = {k: rng.random() for k in keys}
            order = keys[:]
            rng.shuffle(order)
            self.assertEqual(ex.Treap(order, priorities=prios).shape(), ex.priority_order_bst(prios))

    def test_split_merge_round_trip(self) -> None:
        a, b = ex.split(ex.shelf_treap().root, 40)
        self.assertEqual(ex.from_root(ex.merge(a, b)).shape(), ex.shelf_treap().shape())
        t, u = ex.Treap(priorities=ex.ROLLS), ex.Treap(priorities=ex.ROLLS)
        for k in ex.RETURNS:
            t.insert(k)
            u.insert_by_split(k)
        self.assertEqual(t.shape(), u.shape())
        t.delete(25)
        u.delete_by_merge(25)
        self.assertEqual(t.shape(), u.shape())
        self.assertFalse(u.delete_by_merge(26))
        self.assertFalse(u.insert_by_split(58))

    def test_random_against_set(self) -> None:
        rng = random.Random(9)
        t, ref = ex.Treap(seed=3), set()
        for i in range(4000):
            k, op = rng.randrange(300), rng.random()
            if op < 0.4:
                ok = t.insert(k) if i % 2 else t.insert_by_split(k)
                self.assertEqual(ok, k not in ref)
                ref.add(k)
            elif op < 0.7:
                ok = t.delete(k) if i % 2 else t.delete_by_merge(k)
                self.assertEqual(ok, k in ref)
                ref.discard(k)
            else:
                self.assertEqual(t.contains(k), k in ref)
            self.assertTrue(t.valid())
        self.assertEqual(t.keys(), sorted(ref))

    def test_rotations_equal_spines(self) -> None:
        rng = random.Random(4)
        t = ex.Treap(seed=8)
        for k in rng.sample(range(500), 300):
            t.insert(k)
            self.assertEqual(t.last_rotations, ex.spine_rotations(t, k))

    def test_measurements(self) -> None:
        rows = ex.depth_experiment(ex.SHELF, 20_000)
        for k, measured, formula in rows:
            self.assertAlmostEqual(measured, formula, delta=0.05)
        self.assertAlmostEqual(ex.expected_depth(9, 1), 1.829, places=3)
        self.assertAlmostEqual(ex.expected_depth(9, 5), 2.567, places=3)
        self.assertEqual(ex.expected_depth(1, 1), 0)
        measured, exact = ex.rotation_experiment(1000, 200)
        self.assertEqual((round(measured, 3), round(exact, 3)), (1.95, 1.942))
        self.assertEqual(ex.rotation_experiment(1, 3), (0.0, 0.0))
        self.assertAlmostEqual(ex.rotations_per_insert(range(10_000)), 0.9995)
        cmp = ex.library_comparison()
        self.assertEqual([cmp[s][:2] for s in ("treap", "red-black", "splay")], [(20, 32), (16, 15), (999, 33)])
        self.assertEqual([round(cmp[s][2], 2) for s in ("treap", "red-black", "splay")], [15.78, 11.64, 15.69])


if __name__ == "__main__":
    unittest.main()
