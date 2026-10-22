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

    def test_delete_every_case(self) -> None:
        B = ex.BTree
        t = B(3, [58, 25, 84, 12, 47, 70, 91, 31, 63])  # the clearing-out of Section 20.8
        steps = [(47, [[[25, 58, 84]], [[12], [31], [63, 70], [91]]]),    # leaf with a spare key
                 (12, [[[58, 84]], [[25, 31], [63, 70], [91]]]),          # merge with the right sibling
                 (91, [[[58, 70]], [[25, 31], [63], [84]]]),              # borrow from the left sibling
                 (58, [[[31, 70]], [[25], [63], [84]]]),                  # inner key: the predecessor 31 moves up
                 (25, [[[70]], [[31, 63], [84]]]),                        # merge again
                 (84, [[[63]], [[31], [70]]]),                            # borrow again
                 (31, [[[63, 70]]])]                                      # merge empties the root: it shrinks
        for key, levels in steps:
            self.assertTrue(t.delete(key))
            self.assertEqual(t.levels(), levels)
            self.assertTrue(t.valid())
        self.assertEqual((t.borrows, t.merges, t.shrinks, t.height()), (2, 3, 1, 0))
        empty = B(3)
        self.assertEqual((empty.delete(5), empty.levels()), (False, [[[]]]))          # delete from an empty tree
        one = B(3, [5])
        self.assertEqual((one.delete(5), one.levels(), one.valid()), (True, [[[]]], True))  # the only key
        t = B(3, [10, 20, 30, 40, 50])
        before = t.levels()
        self.assertEqual((t.delete(35), t.levels()), (False, before))                 # a missing key
        t = B(3, [1, 2, 3, 4])
        t.delete(4)
        self.assertEqual(t.levels(), [[[2]], [[1], [3]]])
        t.delete(1)                                                                   # merge, then root shrink
        self.assertEqual((t.levels(), t.shrinks), ([[[2, 3]]], 1))
        big = B(3, range(1, 101))
        for k in range(1, 101):
            big.delete(k)
        self.assertEqual((big.levels(), big.merges, big.borrows, big.shrinks), ([[[]]], 90, 3, 5))

    def test_practice_deletes(self) -> None:
        K = [10, 20, 30, 40, 50, 60, 70]
        out = []
        for key in (10, 30, 20):
            t = ex.BTree(3, K)
            t.delete(key)
            out.append(t.levels())
        self.assertEqual(out, [[[[40]], [[20, 30], [50, 60, 70]]], [[[20, 50]], [[10], [40], [60, 70]]],
                               [[[40]], [[10, 30], [50, 60, 70]]]])

    def test_random_insert_delete(self) -> None:
        rng = random.Random(2)
        for m in (3, 5, 7, 9):
            for _ in range(60):
                t, ref = ex.BTree(m), set()
                for _ in range(150):
                    k = rng.randint(0, 120)
                    if rng.random() < 0.5:
                        self.assertEqual(t.delete(k), k in ref)
                        ref.discard(k)
                    else:
                        t.insert(k)
                        ref.add(k)
                    self.assertTrue(t.valid())
                self.assertEqual(t.inorder(), sorted(ref))

    def test_archive(self) -> None:
        self.assertEqual([ex.drawers_opened(2_000_000, f) for f in (250, 167, 125)], [(8000, 3), (11977, 3), (16000, 4)])
        self.assertEqual((ex.drawers_opened(1, 250), ex.drawers_opened(250, 250), ex.drawers_opened(251, 250)),
                         ((1, 1), (1, 1), (2, 2)))

    def test_bottom_up(self) -> None:
        """Figure 20.4: the two ways of splitting can give different trees."""
        keys = [58, 25, 84, 12, 47, 70, 91, 31, 63]
        a, b = ex.BTree(3, keys), ex.BTree(3, keys)
        a.insert(10)
        b.insert_bottom_up(10)
        self.assertEqual(a.levels(), [[[58]], [[25], [84]], [[10, 12], [31, 47], [63, 70], [91]]])
        self.assertEqual(b.levels(), [[[25, 58, 84]], [[10, 12], [31, 47], [63, 70], [91]]])
        a, b = ex.BTree(3, keys), ex.BTree(3, keys)                       # Exercise 20.2
        a.insert(95)
        b.insert_bottom_up(95)
        self.assertEqual(a.levels(), [[[58]], [[25], [84]], [[12], [31, 47], [63, 70], [91, 95]]])
        self.assertEqual(b.levels(), [[[25, 58, 84]], [[12], [31, 47], [63, 70], [91, 95]]])
        c = ex.BTree(3)
        for k in range(1, 101):
            c.insert_bottom_up(k)
        self.assertEqual((c.height(), c.splits, c.valid()), (3, 46, True))
        e = ex.BTree(3)
        e.insert_bottom_up(5)
        e.insert_bottom_up(5)
        self.assertEqual(e.levels(), [[[5]]])

    def test_height_bound(self) -> None:
        """h <= log_t((n + 1) / 2): the half-full rule keeps the tree short (Section 20.7)."""
        import math
        for m in (3, 5, 199):
            t = (m + 1) // 2
            for n in (1, 10, 100, 5000):
                b = ex.BTree(m, range(n))
                self.assertLessEqual(b.height(), math.log((n + 1) / 2, t) + 1e-9)


if __name__ == "__main__":
    unittest.main()
