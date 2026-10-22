import random
import unittest

import ch25_examples as ex


class TestChapter25(unittest.TestCase):
    def test_bookings_tree(self) -> None:
        t = ex.IntervalTree(ex.BOOKINGS)
        self.assertTrue(t.valid())
        self.assertEqual(t.shape()[0], (12, 15, 28))
        self.assertEqual(t.shape()[1][0], (5, 11, 14))
        self.assertEqual(t.shape(), ex.IntervalTree.balanced(ex.BOOKINGS).shape())
        self.assertEqual(t.all_overlaps(*ex.CLOSURE), [(9, 14), (12, 15), (16, 18)])
        self.assertEqual(t.visited, 5)                          # 3-7, 1-2 and 25-28 are never opened (Figure 25.5)
        for q, want, nodes in [((17, 19), (16, 18), 3), ((29, 30), None, 3), ((8, 8), (5, 11), 2)]:
            t.visited = 0
            x = t.find_overlap(*q)
            self.assertEqual((x and x.interval(), t.visited), (want, nodes))

    def test_insert_and_rotate_keep_max(self) -> None:
        t = ex.IntervalTree(ex.BOOKINGS)
        t.insert(17, 19, "poetry group")
        self.assertTrue(t.valid())
        f = t.root.right.left
        self.assertEqual((f.interval(), f.max), ((16, 18), 19))
        t.root.right = ex.rotate_right(t.root.right)           # Figure 25.6, panel 2
        self.assertTrue(t.valid())
        self.assertEqual(ex.shape_of(t.root.right),
                         ((16, 18, 28), None, ((20, 24, 28), ((17, 19, 19), None, None), ((25, 28, 28), None, None))))
        t.root.right = ex.rotate_left(t.root.right)
        self.assertTrue(t.valid())
        self.assertEqual(t.root.right.interval(), (20, 24))
        with self.assertRaises(ValueError):
            t.insert(5, 4)

    def test_every_case(self) -> None:
        t = ex.IntervalTree()                                   # empty tree
        self.assertIsNone(t.find_overlap(1, 5))
        self.assertEqual(t.all_overlaps(1, 5), [])
        self.assertFalse(t.delete(1, 5))
        self.assertTrue(t.valid())
        t.insert(4, 4)                                          # one booking, one day long
        self.assertEqual(t.find_overlap(4, 4).interval(), (4, 4))
        self.assertIsNone(t.find_overlap(5, 9))
        b = ex.IntervalTree(ex.BOOKINGS)
        self.assertEqual(b.all_overlaps(18, 20), [(16, 18), (20, 24)])   # touching ends count: closed intervals
        self.assertEqual(b.all_overlaps(19, 19), [])                      # a gap day: no overlap
        self.assertEqual(b.all_overlaps(0, 40), sorted(iv[:2] for iv in ex.BOOKINGS))   # all overlap
        self.assertEqual(b.all_overlaps(17, 14), [])                      # a backwards query is empty
        self.assertIsNone(b.find_overlap(17, 14))
        self.assertEqual(b.all_overlaps(-9, 0), [])                       # before every booking
        d = ex.IntervalTree([(3, 6), (3, 6), (3, 6)])                    # duplicates
        self.assertEqual(d.all_overlaps(6, 6), [(3, 6)] * 3)
        self.assertTrue(d.delete(3, 6))
        self.assertEqual(d.intervals(), [(3, 6)] * 2)
        self.assertTrue(d.valid())
        for gone in [(1, 2), (3, 7), (12, 15)]:                           # leaf, one child, two children
            self.assertTrue(b.delete(*gone))
            self.assertTrue(b.valid())
        self.assertEqual(b.root.interval(), (16, 18))
        self.assertEqual(b.root.max, 28)
        self.assertFalse(b.delete(12, 15))

    def test_random_against_brute_force(self) -> None:
        rng = random.Random(25)
        for trial in range(300):
            data = ex.random_bookings(rng.randrange(0, 40), days=60, longest=10, seed=trial)
            t = ex.IntervalTree(data) if trial % 2 else ex.IntervalTree.balanced(data)
            for _ in range(rng.randrange(0, 6)):
                if data:
                    gone = data.pop(rng.randrange(len(data)))
                    self.assertTrue(t.delete(*gone))
            self.assertTrue(t.valid())
            self.assertEqual(t.intervals(), sorted(data))
            for _ in range(10):
                lo, hi = sorted(rng.sample(range(-3, 70), 2))
                want = ex.brute_overlaps(data, lo, hi)
                self.assertEqual(t.all_overlaps(lo, hi), want)
                x = t.find_overlap(lo, hi)
                self.assertEqual(x is None, not want)
                if x:
                    self.assertIn(x.interval(), want)

    def test_measure(self) -> None:
        self.assertEqual(ex.measure(), {"n": 1000, "height": 9, "find_one": 5, "k": 16, "all": 25})


if __name__ == "__main__":
    unittest.main()
