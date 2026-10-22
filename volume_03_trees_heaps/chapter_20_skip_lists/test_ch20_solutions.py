import random
import unittest

import ch20_solutions as sol


class TestChapter20Solutions(unittest.TestCase):
    def test_lane_bound(self) -> None:
        self.assertEqual([sol.lane_bound(n) for n in (1, 2, 1000)], [2, 3, 12])
        self.assertEqual(sol.average_lanes(1, trials=2000) <= 2.1, True)        # one key: expected 2 lanes
        for n in (2, 10, 1000):
            self.assertLess(sol.average_lanes(n, trials=300), sol.lane_bound(n))

    def test_kth_smallest_inputs(self) -> None:
        t = sol.RankSkipList()
        self.assertEqual((t.kth(1), t.kth(0)), (None, None))
        t.insert(7)
        self.assertEqual((t.kth(1), t.kth(2)), (7, None))
        self.assertTrue(t.delete(7))
        self.assertEqual((t.kth(1), t.size, t.delete(7)), (None, 0, False))

    def test_kth_returns_pile(self) -> None:
        t = sol.RankSkipList(seed=4)
        for k in [58, 25, 91, 12, 70, 47, 84, 31, 63, 47]:                   # 47 twice: ignored
            t.insert(k)
        self.assertEqual([t.kth(i) for i in range(1, 10)], [12, 25, 31, 47, 58, 63, 70, 84, 91])
        t.delete(58)
        self.assertEqual((t.kth(5), t.kth(8), t.kth(9)), (63, 91, None))

    def test_kth_against_sorted(self) -> None:
        rng = random.Random(7)
        t, ref = sol.RankSkipList(seed=9), set()
        for _ in range(3000):
            k = rng.randint(0, 400)
            if rng.random() < 0.6:
                t.insert(k)
                ref.add(k)
            else:
                self.assertEqual(t.delete(k), k in ref)
                ref.discard(k)
        order = sorted(ref)
        self.assertEqual(t.size, len(order))
        self.assertEqual([t.kth(i) for i in range(1, len(order) + 1)], order)
        self.assertEqual(t.lanes()[0], order)

    def test_counter_heights_bug(self) -> None:
        tidy = sol.counter_heights(list(range(1000)))
        tidy.search_path(499)
        keys = [x for i in range(500) for x in (i, 10_000 + i)]
        bad = sol.counter_heights(keys)
        bad.search_path(499)
        self.assertEqual((tidy.steps, bad.steps), (17, 509))
        self.assertEqual(bad.lanes()[1][0], 10_000)                           # no small key above lane 0


if __name__ == "__main__":
    unittest.main()
