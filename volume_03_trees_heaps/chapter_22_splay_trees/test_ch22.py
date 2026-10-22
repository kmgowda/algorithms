import random
import unittest

import ch22_examples as ex


class TestChapter22(unittest.TestCase):
    def test_every_case(self) -> None:
        t = ex.SplayTree()
        self.assertFalse(t.search(5))                       # empty tree: nothing to splay
        self.assertFalse(t.delete(5))
        self.assertIsNone(t.root)
        self.assertTrue(t.insert(5))                        # one key: no step at all
        self.assertEqual((t.shape(), t.rotations), ((5, None, None), 0))
        self.assertTrue(t.search(5))
        self.assertEqual(t.rotations, 0)                    # already the root
        self.assertFalse(t.insert(5))                       # duplicate: splayed, not added
        self.assertEqual(t.keys(), [5])
        t.insert(3)                                         # one zig
        self.assertEqual(t.steps[-1], "zig")
        self.assertEqual(t.shape(), (3, None, (5, None, None)))
        t = ex.SplayTree([1, 2, 3])                         # left path 3-2-1
        t.search(1)
        self.assertEqual((t.steps[-1], t.shape()), ("zig-zig", (1, None, (2, None, (3, None, None)))))
        t = ex.SplayTree([3, 1])                            # 1 root, 3 right: insert 2 below 3 on the left
        t.insert(2)
        self.assertEqual(t.steps[-1], "zig-zag")
        self.assertEqual(t.shape(), (2, (1, None, None), (3, None, None)))
        t = ex.sorted_build(ex.SHELF)
        self.assertFalse(t.search(40))                      # missing key: the last node visited is splayed
        self.assertEqual(t.root.key, 31)
        self.assertTrue(t.delete(31))
        self.assertEqual(t.root.key, 25)                    # the largest key on the left took its place
        t = ex.SplayTree([12])
        self.assertTrue(t.delete(12))
        self.assertIsNone(t.root)
        t = ex.SplayTree([12, 25])                          # 25 root, no right child after splaying 12
        self.assertTrue(t.delete(12))
        self.assertEqual(t.shape(), (25, None, None))

    def test_shelf_trace(self) -> None:
        t = ex.sorted_build(ex.SHELF)
        self.assertEqual((t.height(), t.root.key), (8, 91))
        r = t.rotations
        t.search(12)
        self.assertEqual(t.steps[-4:], ["zig-zig"] * 4)
        self.assertEqual((t.rotations - r, t.height()), (8, 5))
        self.assertEqual(t.shape(), (12, None, (84, (63, (47, (25, None, (31, None, None)), (58, None, None)),
                                                   (70, None, None)), (91, None, None))))
        shape, height, rot = ex.move_to_root(sorted(ex.SHELF, reverse=True), 12)
        self.assertEqual((height, rot), (8, 8))

    def test_random_against_set(self) -> None:
        rng = random.Random(7)
        t, ref = ex.SplayTree(), set()
        for _ in range(4000):
            k, op = rng.randrange(300), rng.random()
            if op < 0.4:
                self.assertEqual(t.insert(k), k not in ref)
                ref.add(k)
            elif op < 0.7:
                self.assertEqual(t.delete(k), k in ref)
                ref.discard(k)
            else:
                self.assertEqual(t.search(k), k in ref)
            self.assertTrue(t.valid())
        self.assertEqual(t.keys(), sorted(ref))

    def test_access_lemma(self) -> None:
        rng = random.Random(3)
        for trial in range(30):
            keys = list(range(60))
            if trial % 2:
                rng.shuffle(keys)
            t = ex.SplayTree(keys)
            for _ in range(60):
                self.assertGreaterEqual(ex.access_lemma_slack(t, rng.randrange(60)), -1e-9)

    def test_measurements(self) -> None:
        self.assertEqual(ex.sequential_cost(1000), 4374)
        cold, hot = ex.random_workload(10_000, 20_000, hot=0.0), ex.random_workload(10_000, 20_000, hot=0.9)
        self.assertEqual([round(v, 2) for v in cold + hot], [16.21, 17.21, 4.14, 5.14])


if __name__ == "__main__":
    unittest.main()
