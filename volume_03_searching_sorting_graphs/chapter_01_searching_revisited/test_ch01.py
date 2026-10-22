import bisect
import random
import unittest

import ch01_examples as ex


class TestChapter01(unittest.TestCase):
    def test_against_bisect(self) -> None:
        rng = random.Random(1)
        for _ in range(300):
            a = sorted(rng.randint(0, 30) for _ in range(rng.randint(0, 25)))
            for key in range(-2, 33):
                self.assertEqual(ex.lower_bound(a, key), bisect.bisect_left(a, key))
                self.assertEqual(ex.upper_bound(a, key), bisect.bisect_right(a, key))
                self.assertEqual(ex.count(a, key), a.count(key))
                self.assertEqual(ex.contains(a, key), key in a)
            lo, hi = sorted(rng.sample(range(-2, 33), 2))
            self.assertEqual(ex.count_between(a, lo, hi), sum(lo <= x <= hi for x in a))

    def test_catalogue(self) -> None:
        c = ex.CATALOGUE
        t = []
        self.assertEqual(ex.lower_bound(c, 47, t), 4)
        self.assertEqual(t, [(0, 12, 6, 47), (0, 6, 3, 31), (4, 6, 5, 47), (4, 5, 4, 47)])
        self.assertEqual((ex.upper_bound(c, 47), ex.count(c, 47), ex.count_between(c, 30, 65)), (7, 3, 6))
        self.assertEqual((ex.lower_bound(c, 25), ex.upper_bound(c, 25)), (1, 3))
        self.assertEqual((ex.lower_bound(c, 5), ex.lower_bound(c, 95), ex.count_between(c, 40, 80)), (0, 12, 6))
        t = []
        self.assertEqual(ex.lower_bound(c, 63, t), 8)
        self.assertEqual([x[:3] for x in t], [(0, 12, 6), (7, 12, 9), (7, 9, 8), (7, 8, 7)])

    def test_every_case(self) -> None:
        c = ex.CATALOGUE
        table = [([], 7, 0, 0), (c, 5, 0, 0), (c, 95, 12, 12), (c, 31, 3, 4), (c, 47, 4, 7), (c, 50, 7, 7)]
        for a, key, lo, hi in table:
            self.assertEqual((ex.lower_bound(a, key), ex.upper_bound(a, key)), (lo, hi))
            self.assertEqual(ex.contains(a, key), hi > lo)
            t = []
            ex.lower_bound(a, key, t)
            self.assertLessEqual(len(t), 4)

    def test_due_dates(self) -> None:
        rng = random.Random(2)
        due = sorted(rng.randint(1, 365) for _ in range(40_000))
        today, end, new = 172, 178, 175
        got = ex.due_date_report(due, today, end, new)
        self.assertEqual(got[0], due.count(today))
        self.assertEqual(got[1], sum(today <= d <= end for d in due))
        self.assertEqual(got[2], bisect.bisect_right(due, new))

    def test_midpoints(self) -> None:
        self.assertEqual(ex.naive_mid_32bit(2_000_000_000, 2_100_000_000), -97_483_648)
        self.assertEqual(ex.safe_mid(2_000_000_000, 2_100_000_000), 2_050_000_000)
        for lo in range(0, 30):
            for hi in range(lo, 30):
                self.assertEqual(ex.safe_mid(lo, hi), (lo + hi) // 2)
        self.assertEqual(ex.wrap32(2**31), -2**31)


if __name__ == "__main__":
    unittest.main()
