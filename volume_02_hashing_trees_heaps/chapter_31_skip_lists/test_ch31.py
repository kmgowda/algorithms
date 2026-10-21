import random
import unittest

import ch31_examples as ex


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


if __name__ == "__main__":
    unittest.main()
