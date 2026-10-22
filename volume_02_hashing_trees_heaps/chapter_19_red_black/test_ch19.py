import math
import random
import unittest

import ch19_examples as ex


class TestChapter19(unittest.TestCase):
    def test_every_case(self) -> None:
        T = ex.RedBlackTree
        self.assertEqual((T([]).height(), T([5]).shape()), (-1, ((5, "B"), None, None)))
        t = T([5, 3])
        self.assertEqual((t.recolours, t.rotations, t.shape()[1][0]), (0, 0, (3, "R")))
        t = T([2, 1, 3, 4])
        self.assertEqual((t.recolours, t.rotations, t.height()), (1, 0, 2))
        small = ((2, "B"), ((1, "R"), None, None), ((3, "R"), None, None))
        for keys, rot in (([3, 2, 1], 1), ([1, 2, 3], 1), ([3, 1, 2], 2), ([1, 3, 2], 2)):
            t = T(keys)
            self.assertEqual((t.shape(), t.rotations, t.recolours), (small, rot, 0))
        self.assertEqual(T([5, 5]).inorder(), [5])
        big = T(range(1, 101))
        self.assertEqual((big.height(), big.recolours, big.rotations, big.valid()), (10, 87, 89, True))

    def test_delete_cases(self) -> None:
        seven = [12, 25, 31, 47, 58, 63, 70]
        T = ex.RedBlackTree
        t = T()
        self.assertEqual((t.delete(5), t.root), (False, None))                 # empty tree
        t = T(seven)
        self.assertEqual((t.delete(99), t.inorder()), (False, seven))           # missing key
        t = T([5])
        self.assertEqual((t.delete(5), t.root), (True, None))                  # the only key
        for keys, gone, cases, rots, top in (
                ([58], 58, [], 0, (25, "B")),                                  # red leaf: nothing to fix
                ([70, 63], 63, ["red child"], 0, (25, "B")),                   # black node, red child
                ([12], 12, [1, 2], 1, (47, "B")),                              # Figure 19.5
                ([31], 31, [4], 1, (25, "B")),                                 # far red nephew
                ([70, 31], 31, [3, 4], 2, (25, "B")),                          # near red nephew only
                ([25], 25, [4], 1, (31, "B"))):                                # root: successor 31 removed
            t = T(seven)
            for k in keys[:-1]:
                t.delete(k)
            before = t.rotations
            t.delete(keys[-1])
            self.assertEqual((t.cases, t.rotations - before), (cases, rots))
            self.assertEqual(t.shape()[0], top)
            self.assertTrue(t.valid())
            self.assertNotIn(gone, t.inorder())
        t = T(seven)
        r = t.rotations
        t.delete(12)
        self.assertEqual((t.rotations - r, t.shape()),
                         (1, ((47, "B"), ((25, "B"), None, ((31, "R"), None, None)),
                              ((63, "B"), ((58, "R"), None, None), ((70, "R"), None, None)))))
        t = T([10, 20, 30, 40])                                                # Practice Problems 19.3 and 19.4
        t.delete(10)
        self.assertEqual((t.cases, t.shape()), ([4], ((30, "B"), ((20, "B"), None, None), ((40, "B"), None, None))))
        t = T([10, 20, 30, 40])
        t.delete(40)
        t.delete(10)
        self.assertEqual((t.cases, t.shape(), t.black_height()), ([2], ((20, "B"), None, ((30, "R"), None, None)), 1))
        self.assertEqual(T(seven).black_height(), 2)
        self.assertEqual([ex.fewest_keys(h) for h in range(8)], [1, 2, 4, 6, 10, 14, 22, 30])
        self.assertEqual((ex.tallest_height(15), ex.tallest_height(1000), ex.tallest_height(0)), (5, 16, -1))

    def test_measurements(self) -> None:
        rotations, most, seen = ex.random_deletions()                           # Section 19.6
        self.assertEqual((rotations, most), (3761, 3))
        self.assertEqual(seen, {"red child": 2151, 1: 614, 2: 5152, 3: 1038, 4: 2109})

    def test_random_insert_delete(self) -> None:
        rng = random.Random(5)
        most = 0
        for _ in range(300):
            t, keys = ex.RedBlackTree(), set()
            for _ in range(rng.randint(0, 60)):
                k = rng.randint(0, 80)
                if rng.random() < 0.5:
                    t.insert(k)
                    keys.add(k)
                else:
                    r = t.rotations
                    self.assertEqual(t.delete(k), k in keys)
                    most = max(most, t.rotations - r)
                    keys.discard(k)
                self.assertTrue(t.valid())
                self.assertEqual(t.inorder(), sorted(keys))
            self.assertTrue(t.lemma_holds())
            self.assertLessEqual(t.height(), 2 * math.log2(len(keys) + 1))
        self.assertLessEqual(most, 3)                                          # at most three rotations

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
