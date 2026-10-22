import random
import unittest

import ch18_examples as ex


class TestChapter18(unittest.TestCase):
    def test_every_case(self) -> None:
        balanced = (2, (1, None, None), (3, None, None))
        for keys, case in [([3, 2, 1], [("LL", 3)]), ([1, 2, 3], [("RR", 1)]), ([3, 1, 2], [("LR", 3)]),
                           ([1, 3, 2], [("RL", 1)]), ([2, 1, 3], [])]:
            log = []
            self.assertEqual((ex.shape(ex.build(keys, log)), log), (balanced, case))
        self.assertEqual((ex.h(ex.build([])), ex.h(ex.build([5]))), (-1, 0))
        self.assertEqual(ex.inorder(ex.build([5, 5])), [5])
        big = ex.build(range(1, 101))
        self.assertEqual((ex.h(big), ex.is_avl(big), ex.inorder(big)), (6, True, list(range(1, 101))))

    def test_delete_cases(self) -> None:
        self.assertIsNone(ex.delete(None, 5))                                  # empty tree
        t = ex.build([12, 25, 31, 47, 58, 63, 70])
        self.assertEqual(ex.inorder(ex.delete(t, 99)), [12, 25, 31, 47, 58, 63, 70])   # missing key
        self.assertIsNone(ex.delete(ex.build([5]), 5))                         # the only key
        log = []                                                               # a leaf, no repair
        self.assertEqual((ex.shape(ex.delete(ex.build([25, 12, 31]), 12, log)), log),
                         ((25, None, (31, None, None)), []))
        self.assertEqual(ex.shape(ex.delete(ex.build([25, 12, 31, 47]), 31)),  # one child: spliced out
                         (25, (12, None, None), (47, None, None)))
        root = ex.delete(ex.build([12, 25, 31, 47, 58, 63, 70]), 47)           # root, two children: successor
        self.assertEqual((root.key, ex.is_avl(root)), (58, True))
        log = []                                                               # outside, child balanced: LL
        self.assertEqual((ex.shape(ex.delete(ex.build([47, 25, 63, 12, 31]), 63, log)), log),
                         ((25, (12, None, None), (47, (31, None, None), None)), [("LL", 47)]))
        log = []                                                               # inside: LR
        self.assertEqual((ex.shape(ex.delete(ex.build([31, 12, 47, 25]), 47, log)), log),
                         ((25, (12, None, None), (31, None, None)), [("LR", 31)]))
        log = []                                                               # the cascade of Figure 18.6
        t = ex.sparsest(4)
        self.assertEqual((ex.fewest_nodes(4), t.height, ex.is_avl(t)), (12, 4, True))
        t = ex.delete(t, 10, log)
        self.assertEqual((log, t.key, t.height, ex.is_avl(t)), ([("RR", 20), ("RR", 50)], 80, 3, True))
        self.assertEqual([ex.fewest_nodes(k) for k in range(7)], [1, 2, 4, 7, 12, 20, 33])

    def test_measurements(self) -> None:
        self.assertEqual(ex.random_deletions(), (2645, 3, 3684))                  # Section 18.8
        self.assertEqual([ex.cascade(h) for h in (2, 4, 6, 8, 10)], [1, 2, 3, 4, 5])
        log = []
        self.assertEqual((ex.build(range(1, 101), log).height, len(log)), (6, 93))

    def test_random_insert_delete(self) -> None:
        rng = random.Random(2)
        for _ in range(300):
            t, keys = None, set()
            for _ in range(rng.randint(0, 60)):
                k = rng.randint(0, 50)
                if rng.random() < 0.55:
                    t = ex.insert(t, k)
                    keys.add(k)
                else:
                    t = ex.delete(t, k)
                    keys.discard(k)
                self.assertTrue(ex.is_avl(t))
                self.assertEqual(ex.inorder(t), sorted(keys))

    def test_avl(self) -> None:
        log = []
        t = ex.build([12, 25, 31, 47, 58, 63, 70], log)
        self.assertEqual(t.height, 2)
        self.assertEqual(log, [("RR", 12), ("RR", 31), ("RR", 25), ("RR", 58)])
        log = []
        self.assertEqual(ex.shape(ex.build([50, 40, 30, 20, 10], log)),
                         (40, (20, (10, None, None), (30, None, None)), (50, None, None)))
        self.assertEqual(ex.shape(ex.build([10, 30, 20])), (20, (10, None, None), (30, None, None)))
        self.assertEqual(ex.build(range(1000)).height, 9)
        rng = random.Random(1)
        for _ in range(100):
            keys = [rng.randint(0, 200) for _ in range(rng.randint(1, 60))]
            t = ex.build(keys)
            self.assertTrue(ex.is_avl(t))
            self.assertEqual(ex.inorder(t), sorted(set(keys)))


if __name__ == "__main__":
    unittest.main()
