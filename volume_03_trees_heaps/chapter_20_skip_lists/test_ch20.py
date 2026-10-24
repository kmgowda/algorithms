import random
import unittest

import ch20_examples as ex


class TestChapter60(unittest.TestCase):
    def test_every_case(self) -> None:
        s = ex.SkipList()
        s.search_path(5)
        self.assertEqual((s.contains(5), s.steps), (False, 1))
        for k in (12, 25, 47, 58, 63):
            s.insert(k)
        self.assertEqual(s.lanes(), [[12, 25, 47, 58, 63], [12, 47, 63], [47, 63], [47]])
        self.assertEqual([s.contains(k) for k in (12, 63, 50, 5, 99)], [True, True, False, False, False])
        self.assertEqual((s.search_path(63), s.search_path(5)), ([(3, 47), (0, 58)], []))
        s.insert(47)
        self.assertEqual(s.lanes()[0], [12, 25, 47, 58, 63])
        flat, rnd = ex.SkipList(fixed_levels={k: 1 for k in range(1000)}), ex.SkipList(seed=1)
        for k in range(1000):
            flat.insert(k)
            rnd.insert(k)
        steps = []
        for lst, key in ((rnd, 999), (rnd, 0), (flat, 999), (flat, 0)):
            lst.search_path(key)
            steps.append(lst.steps)
        self.assertEqual((len(rnd.lanes()), steps), (14, [27, 14, 1000, 1]))

    def test_against_sorted_set(self) -> None:
        rng = random.Random(1)
        s, ref = ex.SkipList(seed=5), set()
        for _ in range(2000):
            k = rng.randint(0, 500)
            s.insert(k)
            ref.add(k)
        self.assertEqual(s.lanes()[0], sorted(ref))
        for lane in s.lanes():
            self.assertEqual(lane, sorted(lane))
            self.assertTrue(set(lane) <= ref)
        for k in range(0, 520, 7):
            self.assertEqual(s.contains(k), k in ref)

    def test_figure(self) -> None:
        lv = {12: 1, 25: 3, 31: 1, 47: 2, 58: 4, 63: 1, 70: 2, 84: 3, 91: 1}
        s = ex.SkipList(fixed_levels=lv)
        for k in lv:
            s.insert(k)
        self.assertEqual(s.lanes()[1:], [[25, 47, 58, 70, 84], [25, 58, 84], [58]])
        self.assertEqual(s.search_path(70), [(3, 58), (0, 63)])
        self.assertEqual(s.search_path(47), [(2, 25), (0, 31)])
        self.assertEqual(s.search_path(91), [(3, 58), (2, 84)])

    def test_delete_every_case(self) -> None:
        self.assertEqual(ex.SkipList().delete(5), [])                       # empty list
        lv = {12: 1, 25: 3, 31: 1, 47: 2, 58: 4, 63: 1, 70: 2, 84: 3, 91: 1}
        s = ex.SkipList(fixed_levels=lv)
        for k in lv:
            s.insert(k)
        self.assertEqual(s.delete(50), [])                                  # missing key
        self.assertEqual(s.delete(58), [(3, None), (2, 25), (1, 47), (0, 47)])   # the key on the top lane
        self.assertEqual((s.level, s.lanes()[1:]), (3, [[25, 47, 70, 84], [25, 84]]))
        self.assertEqual(s.delete(12), [(2, None), (1, None), (0, None)])   # the first key
        self.assertFalse(s.contains(58) or s.contains(12))
        one = ex.SkipList(fixed_levels={7: 3})
        one.insert(7)
        one.delete(7)                                                       # the only key
        self.assertEqual((one.lanes(), one.level, one.contains(7)), ([[]], 1, False))

    def test_delete_against_set(self) -> None:
        rng = random.Random(2)
        s, ref = ex.SkipList(seed=7), set()
        for _ in range(4000):
            k = rng.randint(0, 300)
            if rng.random() < 0.5:
                s.insert(k)
                ref.add(k)
            else:
                self.assertEqual(bool(s.delete(k)), k in ref)
                ref.discard(k)
        self.assertEqual(s.lanes()[0], sorted(ref))
        for lane in s.lanes():
            self.assertEqual(lane, sorted(lane))

    def test_leaderboard(self) -> None:
        rng = random.Random(3)
        points = {r: rng.randint(0, 600) for r in range(3000)}
        board = ex.SkipList(seed=4)
        for r, p in points.items():
            board.insert((p, r))
        for _ in range(3000):                                               # a points change: delete, re-insert
            r = rng.randrange(3000)
            board.delete((points[r], r))
            points[r] += rng.randint(-20, 40)
            board.insert((points[r], r))
        want = sorted((p, r) for r, p in points.items() if 300 <= p <= 400)
        self.assertEqual(board.range_keys((300, -1), (400, 10 ** 9)), want)
        self.assertEqual(board.range_keys((10 ** 6, 0), (10 ** 7, 0)), [])


    def test_veb(self) -> None:
        import bisect
        import random
        v = ex.VEB(16)
        for k in [2, 3, 4, 5, 7, 14, 15]:
            v.insert(k)
        self.assertTrue(v.member(7))
        self.assertFalse(v.member(6))
        self.assertEqual([v.successor(x) for x in (0, 5, 7, 13, 15)], [2, 7, 14, 14, None])
        r = random.Random(20)
        for u in (2, 4, 16, 256, 4096):
            for _ in range(20):
                keys = r.sample(range(u), r.randint(0, min(u, 60)))
                v = ex.VEB(u)
                for k in keys:
                    v.insert(k)
                srt = sorted(keys)
                for x in range(-1, u):
                    if x >= 0:
                        self.assertEqual(v.member(x), x in keys)
                    i = bisect.bisect_right(srt, x)
                    self.assertEqual(v.successor(x), srt[i] if i < len(srt) else None)


if __name__ == "__main__":
    unittest.main()
